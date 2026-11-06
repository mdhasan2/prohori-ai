
export type ApprovalGate = 'investigation' | 'validation'

export interface PendingApproval {
    gate: ApprovalGate
    binding: string
    asset_id: string
    operation: string
    proposal: Record<string, unknown> | null
}

export interface WorkflowState {
    status?: string
    hypothesis?: Record<string, unknown>
    proposal?: Record<string, unknown>
    evidence?: Record<string, unknown>[]
    finding?: Record<string, unknown>
    error?: string
}

export interface RunResponse {
    run_id: string
    status: string
    pending_approval: PendingApproval | null
    state: WorkflowState
    stopped: boolean
}

export interface DecisionRequest {
    expected_gate: ApprovalGate
    expected_binding: string
    approved: boolean
}

export interface AuditEvent {
    id: number
    at: string
    action: string
    details: Record<string, unknown>
}

export interface HealthResponse {
    status: 'ok'
}

export interface StopResponse {
    stopped: boolean
}
