import "@testing-library/jest-dom/vitest"
import { render, screen, waitFor } from "@testing-library/react"
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest"
import App from "./App"

const fetchMock = vi.fn<typeof fetch>()

beforeEach(() => {
    localStorage.clear()
    fetchMock.mockReset()
    fetchMock.mockResolvedValue(
        new Response(
            JSON.stringify({
                status: 'ok',
                access_mode: 'local_only',
            }),
            {
                status: 200,
                headers: { 'Content-Type': 'application/json' },
            },
        ),
    )
    vi.stubGlobal('fetch', fetchMock)
})

afterEach(() => {
    vi.unstubAllGlobals()
})

describe('Security Control Center foundation', () => {
    it('provides an accessible page identity', async () => {
        render(<App />)

        expect(screen.getByRole('main')).toBeInTheDocument()
        expect(
            screen.getByRole('heading', {
                level: 1,
                name: 'Security Control Center',
            }),
        ).toBeInTheDocument()

        expect(screen.getByRole('status')).toHaveTextContent(
            'API mode: Unconfirmed.',
        )

        await waitFor(() => {
            expect(screen.getByRole('status')).toHaveTextContent(
                'Backend: Connected. API mode: Local-only.',
            )
        })

        expect(fetchMock).toHaveBeenCalledWith(
            '/api/health',
            expect.objectContaining({
                headers: { Accept: 'application/json' },
            }),
        )

        expect(
            screen.getByRole('button', { name: 'New investigation' }),
        ).toBeInTheDocument()
    })

    it('shows a denied request without confirming access', async() =>{
        fetchMock.mockResolvedValue(
            new Response(
                JSON.stringify({ detail: 'Local operator access only.' }),
                {
                    status: 403,
                    headers: { 'Contetn-Type': 'application/json' },
                },
            ),
        )

        render(<App />)

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'Local operator access only.',
        )
        expect(screen.getByRole('status')).toHaveTextContent(
            'Backend: Unavailable. API mode: Unconfirmed.',
        )
    })

    it('rejects an older or incomplete health contract', async () => {
        fetchMock.mockResolvedValue(
            new Response(JSON.stringify({ status: 'ok' }), {
                status: 200,
                headers: { 'Content-Type': 'application/json' },
            }),
        )

        render(<App />)

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'Backend did not confirm local-only access.',
        )
        expect(screen.getByRole('status')).toHaveTextContent(
            'API mode: Unconfirmed.',
        )
    })

    it('reports a network failure', async () => {
        fetchMock.mockRejectedValue(new Error('Network unavailable'))

        render(<App />)

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'Network unavailable',
        )
        expect(screen.getByRole('status')).toHaveTextContent(
            'API mode: Unconfirmed.',
        )
    })
})