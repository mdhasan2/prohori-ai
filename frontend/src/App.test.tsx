import "@testing-library/jest-dom/vitest"
import {
    fireEvent,
    render,
    screen,
    waitFor
} from "@testing-library/react"
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
                identity_mode: 'unconfigured',
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

    it.each([undefined, 'authenticated'])(
        'rejects an unsupported identity mode: %s',
        async (identityMode) => {
            fetchMock.mockResolvedValue(
                new Response(
                    JSON.stringify({
                        status: 'ok',
                        access_mode: 'local_only',
                        identity_mode: identityMode,
                    }),
                    {
                        status: 200,
                        headers: {
                            'Content-Type': 'application/json',
                        },
                    },
                ),
            )

            render(<App />)

            expect(await screen.findByRole('alert')).toHaveTextContent(
                'Backend did not confirm the operator identity mode.',
            )

            expect(
                screen.getByText('Operator identity: unconfirmed.'),
            ).toBeInTheDocument()
        },
    )

    it('keeps run input while navigating without API mutations', async () => {
        render(<App />)

        expect(
            await screen.findByText(
                'Operator identity: not configured.',
            ),
        ).toBeInTheDocument()

        const input = screen.getByRole('textbox', {
            name: 'Run ID',
        })

        fireEvent.change(input, {
            target: { value: 'draft-run-id' },
        })

        const assets = screen.getByRole('link', {
            name: 'Asset inventory',
        })
        const investigations = screen.getByRole('link', {
            name: 'Investigations',
        })

        expect(assets).toHaveAttribute('href', '#inventory-section')
        expect(investigations).toHaveAttribute(
            'href',
            '#investigation-controls',
        )

        expect(
            document.getElementById('inventory-section'),
        ).toBeInTheDocument()
        expect(
            document.getElementById('investigation-controls'),
        ).toBeInTheDocument()

        fireEvent.click(assets)
        fireEvent.click(investigations)

        expect(input).toHaveValue('draft-run-id')
        expect(
            screen.getByRole('button', { name: 'Emergency stop' }),
        ).toBeVisible()

        expect(fetchMock).toHaveBeenCalledTimes(1)
    })
})