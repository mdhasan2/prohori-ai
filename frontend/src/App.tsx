import { useEffect, useRef, useState } from 'react'
import {
  activateStop,
  createRun,
  getAudit,
  getHealth,
  getRun,
  submitDecision,
} from './api/client'

import type {
  AuditEvent,
  HealthResponse,
  RunResponse,
 } from './api/types'

import ApprovalPanel from './components/ApprovalPanel'
import InvestigationResult from './components/InvestigationResult'
import AuditTimeline from './components/AuditTimeline'

const STORAGE_KEY = 'prohori:lastRunId'

function message(error: unknown): string {
  return error instanceof Error ? error.message: 'Unexpected error'
}

function savedRunId(): string {
  try {
    return localStorage.getItem(STORAGE_KEY) ?? ''
  } catch {
    return ''
  }
}

function saveRunId(id: string) {
  try {
    localStorage.setItem(STORAGE_KEY, id)
  } catch {
    // The workflow still works when browser storage is unavailable.
  }
}

export default function App() {
  const [connection, setConnection] = useState('Checking')
  const [accessMode, setAccessMode] = 
  useState<HealthResponse['access_mode'] | null>(null)
  const [healthError, setHealthError] = useState('')
  const [run, setRun] = useState<RunResponse | null>(null)
  const [runId, setRunId] = useState('')
  const [audit, setAudit] = useState<AuditEvent[]>([])
  const [busy, setBusy] = useState(false)
  const [stopping, setStopping] = useState(false)
  const [stopped, setStopped] = useState(false)
  const [error, setError] = useState('')
  const [auditError, setAuditError] = useState('')
  const [needsRefresh, setNeedRefresh] = useState(false)
  const actionLock = useRef(false)
  const stopLock = useRef(false)
  
  useEffect(() => {
    let active = true

    async function initialize() {
      try {
        const health = await getHealth()

        if (active) {
          setConnection('Connected')
          setAccessMode(health.access_mode)
          setHealthError('')
        }
      } catch (cause) {
        if (active) {
          setConnection('Unavailable')
          setAccessMode(null)
          setHealthError(message(cause))
        }
      }
      
      const id = savedRunId()
      if (!id) return

      try {
        const restored = await getRun(id)
        if (!active) return
        setRun(restored)
        setRunId(restored.run_id)
        setStopped(restored.stopped)

        try {
          const events = await getAudit(id)
          if (active) setAudit(events)
        } catch (cause) {
          if (active) setAuditError(message(cause))
        }
      } catch (cause) {
        if (active) setError(message(cause))
      }
    }

    void initialize()
    return () => {
      active =false
    }
  }, [])

  async function perform(
    operation: () => Promise<RunResponse>,
    mutation: boolean,
  ) {
    if (actionLock.current) return
    actionLock.current = true
    setBusy(true)
    setError('')
    setAuditError('')

    try {
      const updated = await operation()
      setRun(updated)
      setRunId(updated.run_id)
      setStopped(updated.stopped || stopLock.current)
      saveRunId(updated.run_id)
      setNeedRefresh(false)
      setConnection('Connected')
      setAudit([])

      // A failed audit read must not imply that the decision failed.
      try {
        setAudit(await getAudit(updated.run_id))
      } catch (cause) {
        setAuditError(message(cause))
      }
    } catch (cause) {
      setError(message(cause))
      if (mutation) setNeedRefresh(true)
    } finally {
      actionLock.current = false
      setBusy(false)
    }
  }

  function decide(approved: boolean) {
    const pending = run?.pending_approval
    if (!run || !pending) return

    void perform(
      () =>
        submitDecision(run.run_id, {
          expected_gate: pending.gate,
          expected_binding: pending.binding,
          approved,
        }),
      true,
    )
  }

  async function stop() {
    if (stopLock.current) return
    stopLock.current = true
    setStopping(true)
    try {
      await activateStop()
      setStopped(true)
    } catch (cause) {
      setError(`Emergency stop was not confirmed: ${message(cause)}`)
    } finally {
      stopLock.current = false
      setStopping(false)
    }
  }

  const pending = run?.pending_approval

  return (
    <main>
      <header>
        <p>Prohori AI</p>
        <h1>Security Control Center</h1>
        <p role="status" aria-live="polite">
          Backend: {connection}. API mode:{' '}
          {accessMode === 'local_only' ? 'Local-only': 'Unconfirmed'}.
        </p>
        <p>Operator identity: not configured.</p>
        {healthError && <p role="alert">{healthError}</p>}
      </header>

      <section aria-label="Investigation controls">
        <button
          disabled={busy || stopped || needsRefresh}
          onClick={() => void perform(createRun, true)}
        >
          New investigation
        </button>

        <label htmlFor="run-id"> Run ID</label>
        <input
          id="run-id"
          value={runId}
          onChange={(event) => setRunId(event.target.value)}
          placeholder='Paste a run UUID'
        />

        <button
          disabled={busy || !runId.trim()}
          onClick={() =>
            void perform(() => getRun(runId.trim()), false)
          }
        >
          Open / refresh run
        </button>

        <button
          className="danger"
          disabled={stopping || stopped}
          onClick={() => void stop()}
        >
          {stopping ? 'Stopping...' : 'Emergency stop'}
        </button>
      </section>

      {busy && <p role="status">Processing...</p>}
      {error && <p role="alert">{error}</p>}
      {needsRefresh && (
        <p>
          The last action could not be confirmed. Refresh the run before
          submitting another decision. If creation failed before returning
          a run ID, check the backend before starting another run.
        </p>
      )}
      {stopped && (
        <p role="status">
          Emergency stop is active. Subsequent tool attempts are blocked.
        </p>
      )}

      {run && (
        <>
          <section>
            <h2>Investigation</h2>
            <p>Run: {run.run_id}</p>
            <p>Status: {run.status}</p>
            <p>Target: http://127.0.0.1:18080/</p>
            <p>Check: Content-Security-Policy response header </p>
            {run.status === 'interrupted' && (
              <p>
                Execution was interrupted outside and approval gate.
                This interface cannot safely resume it.
              </p>
            )}
          </section>
          
          {pending && (
            <ApprovalPanel
              pending={pending}
              busy={busy}
              stopped={stopped}
              needsRefresh={needsRefresh}
              onDecision={decide}
            />
          )}

          <InvestigationResult state={run.state} />

          <AuditTimeline events={audit} error={auditError}/>
        </>
      )}
    </main>
  )
}