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
    access_mode: 'local_only'
    identity_mode: 'unconfigured'
}

export interface StopResponse {
    stopped: boolean
}

export const ASSET_TYPES = [
    'server',
    'application',
    'api',
    'container',
    'kubernetes_workload',
    'cloud_resource',
    'ai_agent',
] as const

export type AssetType = (typeof ASSET_TYPES)[number]

export const ASSET_ENVIRONMENTS = [
    'unknown',
    'lab',
    'development',
    'staging',
    'production',
] as const

export type AssetEnvironment = (typeof ASSET_ENVIRONMENTS)[number]

export const DATA_CLASSIFICATIONS = [
    'unknown',
    'public',
    'internal',
    'confidential',
    'restricted',
] as const

export type DataClassification = (typeof DATA_CLASSIFICATIONS)[number]

export const DISCOVERY_SOURCES = [
    'unknown',
    'demo_fixture',
] as const

export type DiscoverySource = (typeof DISCOVERY_SOURCES)[number]

export interface SecurityAsset {
    asset_id: string
    name: string
    asset_type: AssetType
    owner_team: string | null
    environment: AssetEnvironment
    data_classification: DataClassification
    discovery_source: DiscoverySource
    record_origin: 'synthetic'
    verification_state: 'unverified'
}