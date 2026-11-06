import type { AuditEvent } from "../api/types"

interface AuditTimelineProps {
    events: AuditEvent[]
    error?: string
}

export default function AuditTimeline({
    events,
    error,
}: AuditTimelineProps) {
    return (
        <section aria-labelledby='audit-heading'>
            <h2 id="audit-heading">Audit timeline</h2>

            {error && <p role='alert'> {error}</p>}
            
            {events.length === 0 ? (
                <p>No audit events loaded.</p>
            ) : (
            <ol>
              {events.map((event) => (
                <li key={event.id}>
                  <strong>{event.action}</strong>
                  {' — '}
                  <time dateTime={event.at}>{event.at}</time>

                  <details>
                    <summary>Event details</summary>
                    <pre>{JSON.stringify(event.details, null, 2)}</pre>
                  </details>
                </li>
              ))}
            </ol>
            )}
        </section>
    )
}