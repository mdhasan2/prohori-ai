type DataMode = 'demo'

interface EnvironmentNoticeProps {
  mode: DataMode
}

function EnvironmentNotice({ mode }: EnvironmentNoticeProps) {
  return (
    <section aria-labelledby='environment-heading'>
      <h2 id='environment-heading'>Environment</h2>
      <dl>
        <div>
          <dt>Data mode</dt>
          <dd>{mode}</dd>
        </div>
        <div>
          <dt>Backend connection</dt>
          <dd>Not connected</dd>
        </div>
      </dl>
      <p>
        This foundation page does not initiate investigations or execute
        security tools.
      </p>
    </section>
  )
}

export default function App() {
  return (
    <main>
      <header>
        <p>Prohori-AI</p>
        <h1>Security Control Center</h1>
        <p>Human-governed security investigation workspace</p>
      </header>

      <EnvironmentNotice mode='demo' />

      <section aria-labelledby='progress-heading'>
        <h2 id='progress-heading'>Implementaion progress</h2>
        <p>UI-01: React and TypeScript foundation</p>
        <p>Live backend integration has not been implemented.</p>
      </section>
    </main>
  )
}
