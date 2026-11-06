import type { PendingApproval } from "../api/types"

interface ApprovalPanelProps {
    pending: PendingApproval
    busy: boolean
    stopped: boolean
    needsRefresh: boolean
    onDecision: (approved: boolean) => void
}

export default function ApprovalPanel({
    pending,
    busy,
    stopped,
    needsRefresh,
    onDecision
}: ApprovalPanelProps) {
    return (
        <section aria-labelledby='approval-heading'>
            <h2 id='approval-heading'>
                {pending.gate === 'investigation'
                    ? 'Investigation approval'
                    : 'Validation approval'}
            </h2>

            <p>Asset: {pending.asset_id}</p>
            <p>{pending.operation}</p>

            <details>
                <summary>Approval binding</summary>
                <code>{pending.binding}</code>
            </details>

            {pending.proposal && (
                <>
                    <h3>Validation proposal</h3>
                    <pre>{JSON.stringify(pending.proposal, null, 2)}</pre>
                </>
            )}

            <button
                disabled={busy || stopped || needsRefresh}
                onClick={() => onDecision(true)}
            >
                Approve {pending.gate}
            </button>
            
            <button
                disabled={busy || stopped || needsRefresh}
                onClick={() => onDecision(false)}
            >
                Reject {pending.gate}
            </button>
        </section>
    )
}


        
