import type {
    AuditEvent,
    DecisionRequest,
    HealthResponse,
    RunResponse,
    StopResponse,
} from './types'

export class ApiError extends Error {
    readonly status: number

    constructor(status: number, message: string) {
        super(message)
        this.name = 'ApiError'
        this.status = status
    }
}

function errorMessage(body: unknown, fallback: string): string {
    if (typeof body !== 'object' || body === null) return fallback

    const detail = (body as Record<string, unknown>).detail

    if (typeof detail === 'string') return detail

    // FastAPI validation errors have an array-valued detail.
    if (Array.isArray(detail)) return JSON.stringify(detail)

    return fallback
}

async function request<T>(
    path: string,
    options: RequestInit = {},
): Promise<T> {
    const response = await fetch(`/api${path}`, {
        ...options,
        headers: {
            Accept: 'application/json',
            ...options.headers,
        },
    })

    const body: unknown = await response.json().catch(() => null)

    if (!response.ok) {
        throw new ApiError(
            response.status,
            errorMessage(body, `Request failed (${response.status})`),
        )
    }

    if (body === null) {
        throw new ApiError(response.status, 'Server returned invalid JSON.')
    }

    // Compile-time typing only; the backend validates its response models.
    return body as T

}

function post<T>( path: string, body: unknown): Promise<T> {
    return request<T>(path, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
    })
}

export async function getHealth(): Promise<HealthResponse> {
    const body = await request<unknown>('/health')

    if(
        typeof body !== 'object' ||
        body === null ||
        !('status' in body) ||
        body.status !== 'ok' ||
        !('access_mode' in body) ||
        body.access_mode !== 'local_only'
    ) {
        throw new Error('Backend did not confirm local-only access.')
    }

    return {
        status: 'ok',
        access_mode: 'local_only',
    }
}

export function createRun(): Promise<RunResponse> {
    return post('/runs', {})
}

export function getRun(runId: string): Promise<RunResponse> {
    return request(`/runs/${encodeURIComponent(runId)}`)
}

export function submitDecision(
    runId: string,
    decision: DecisionRequest,
): Promise<RunResponse> {
    return post(`/runs/${encodeURIComponent(runId)}/decision`, decision)
}

export function getAudit(runId: string): Promise<AuditEvent[]> {
    return request(`/runs/${encodeURIComponent(runId)}/audit`)
}

export function activateStop(): Promise <StopResponse> {
    return post('/stop', {})
}