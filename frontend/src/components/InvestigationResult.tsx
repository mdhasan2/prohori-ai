import type { WorkflowState } from "../api/types";

interface InvestigationResultProps {
    state: WorkflowState
}

export default function InvestigationResult({
    state,
}: InvestigationResultProps) {
    const evidence = state.evidence ?? []

    return (
        <section aria-labelledby='result-heading'>
            <h2 id="result-heading">Evidence and result</h2>

            {state.error && <p role="alert">{state.error}</p>}

            {state.hypothesis && (
                <>
                    <h3>Hypothesis</h3>
                    <pre>{JSON.stringify(state.hypothesis, null, 2)}</pre>
                </>
            )}
            
            {evidence.length == 0 ? (
                <p>No evidence has been collected.</p>
            ) : (
                <ol>
                    {evidence.map((item, index) => (
                        <li
                            key={
                                typeof item.evidence_id === 'string'
                                    ? item.evidence_id
                                    : index
                            }
                        >
                            <pre>{JSON.stringify(item, null, 2)}</pre>
                        </li>
                    ))}
                </ol>
            )}

            <h3>Finding</h3>

            {state.finding ? (
                <pre>{JSON.stringify(state.finding, null, 2)}</pre>
            ) : (
                <p>No finding has been recorded</p>
            )}

            <details>
                    <summary>Full workflow state</summary>
                    <pre>{JSON.stringify(state, null, 2)}</pre>
            </details>

        </section>
    )
}

