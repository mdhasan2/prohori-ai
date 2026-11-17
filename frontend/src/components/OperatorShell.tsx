import type { ReactNode } from "react"
import type { HealthResponse } from "../api/types"
import '../styles/operator-shell.css'

interface OperatorShellProps {
    connection: string
    accessMode: HealthResponse['access_mode'] | null
    identityMode: HealthResponse['identity_mode'] | null
    healthError: string
    children: ReactNode
}

export default function OperatorShell({
    connection,
    accessMode,
    identityMode,
    healthError,
    children,
}: OperatorShellProps) {
    return (
        <div className="operator-shell">
            <a className="operator-skip-link" href="#console-main">
                Skip to console
            </a>

            <aside className="operator-rail">
                <span className="operator-monogram" aria-hidden="true">
                    PA
                </span>

                <nav aria-label="Console navigation">
                    <a
                        href="#inventory-section"
                        aria-label="Asset inventory"
                        title="Asset inventory"
                    >
                        <svg
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.8"
                            aria-hidden="true"
                            focusable="false"
                        >
                            <rect x="3" y="3" width="7" height="7" rx="1" />
                            <rect x="14" y="3" width="7" height="7" rx="1" />
                            <rect x="3" y="14" width="7" height="7" rx="1" />
                            <rect x="14" y="14" width="7" height="7" rx="1" />
                        </svg>
                    </a>
                    <a
                        href="#investigation-controls"
                        aria-label="Investigations"
                        title="Investigations"
                    >
                        <svg
                            viewBox="0 0 24 24"
                            fill="none"
                            stroke="currentColor"
                            strokeWidth="1.8"
                            aria-hidden="true"
                            focusable="false"
                        >
                            <circle cx="10" cy="10" r="6" />
                            <path d="m15 15 6 6" />                            
                        </svg>
                    </a>
                </nav>
            </aside>
            <main
                id="console-main"
                className="operator-main"
                tabIndex={-1}
            >
                <header className="operator-header">
                    <p className="operator-eyebrow"> Prohori AI</p>
                    <h1>Security Control Center</h1>

                    <p role="status" aria-live="polite">
                        Backend: {connection}. API mode: {' '}
                        {accessMode === 'local_only'
                            ? 'Local-only'
                            : 'Unconfirmed'}.
                    </p>

                    <p className="operator-identity">
                        Operator identity:{' '}
                        {identityMode === 'unconfigured'
                            ? 'not configured'
                            : 'unconfirmed'}.
                    </p>

                    {healthError && (
                        <p role="alert">{healthError}</p>
                    )}
                </header>

                {children}
            </main>
        </div>
    )
}