import { fireEvent, render, screen } from "@testing-library/react"
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest"
import App from '../App'
import type { SecurityAsset } from "../api/types"
import InventoryPanel from "./InventoryPanel"

const asset: SecurityAsset = {
    asset_id: 'lab-api',
    name: 'Path-traversal lab API',
    asset_type: 'api',
    record_origin: 'synthetic',
    verification_state: 'unverified',
}

const fetchMock = vi.fn<typeof fetch>()

function jsonResponse(body: unknown, status = 200): Response {
    return new Response(JSON.stringify(body), {
        status,
        headers: { 'Content-Type': 'application/json'},
    })
}

beforeEach(() => {
    fetchMock.mockReset()
    fetchMock.mockImplementation(async () => jsonResponse([asset]))
    vi.stubGlobal('fetch', fetchMock)
})

afterEach(() => {
    vi.unstubAllGlobals()
})

function loadInventory() {
    fireEvent.click(
        screen.getByRole('button', { name: 'Load lab inventory' }),
    )
}

describe('InventoryPanel', ()=> {
    it('loads only on request and labels the demo record', async () => {
        render(<InventoryPanel/>)

        expect(screen.getByText('Inventory not loaded.')).toBeInTheDocument()
        expect(fetchMock).not.toHaveBeenCalled()

        loadInventory()

        expect(screen.getByRole('status')).toHaveTextContent(
            'Loading inventory...',
        )

        expect(
            await screen.findByRole('heading', {
                name: 'Path-traversal lab API',
            }),
        ).toBeInTheDocument()

        expect(screen.getByText('Synthetic demo record')).toBeInTheDocument()
        expect(screen.getByText('Verification: unverified')).toBeInTheDocument()

        expect(fetchMock).toHaveBeenCalledWith(
            '/api/assets',
            expect.objectContaining({
                headers: { Accept: 'application/json' },
            }),
        )
    })

    it('shows an access denial without displaying records', async () => {
        fetchMock.mockResolvedValue(
            jsonResponse({ detail: 'Local operator access only.' }, 403),
        )

        render(<InventoryPanel />)
        loadInventory()

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'Local operator access only.',
        )
        expect(
            screen.queryByRole('heading', { name: asset.name }),
        ).not.toBeInTheDocument()
    })

    it('rejects an unsupported verification claim', async () => {
        fetchMock.mockResolvedValue(
            jsonResponse([{ ...asset, verification_state: 'verified' }]),
        )

        render(<InventoryPanel />)
        loadInventory()

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'Server returned an invalid inventory response.',
        )
    })

    it('distinguishes an empty inventory from an error', async () => {
        fetchMock.mockResolvedValue(jsonResponse([]))

        render(<InventoryPanel />)
        loadInventory()

        expect(
            await screen.findByText('No asset records returned.'),
        ).toBeInTheDocument()
        expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    })

    it('allows a retry after a network failure', async () => {
        fetchMock.mockRejectedValueOnce(new Error('Network unavailable'))

        render(<InventoryPanel />)
        loadInventory()

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'Network unavailable',
        )

        loadInventory()

        expect(
            await screen.findByRole('heading', { name: asset.name }),
        ).toBeInTheDocument()
        expect(screen.queryByRole('alert')).not.toBeInTheDocument()
    })

    it('works inside App without starting an investigation', async () => {
        localStorage.clear()

        fetchMock.mockImplementation(async (input) => {
            if(input === '/api/health') {
                return jsonResponse({
                    status: 'ok',
                    access_mode: 'local_only',
                })
            }

            if (input === '/api/assets') {
                return jsonResponse([asset])
            }

            throw new Error(`Unexpected request: ${String(input)}`)
        })

        render(<App />)
        loadInventory()

        expect(
            await screen.findByRole('heading', { name: asset.name }),
        ).toBeInTheDocument()
        expect(
            screen.getByRole('button', { name: 'New investigation' }),
        ).toBeInTheDocument()

        for (const [, options] of fetchMock.mock.calls) {
            expect(options?.method ?? 'GET').toBe('GET')
        }
    })

})