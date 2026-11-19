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
    owner_team: null,
    environment: 'lab',
    data_classification: 'unknown',
    discovery_source: 'demo_fixture',
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

        expect(
            screen.getByText('Owner team: Unknown (not recorded)'),
        ).toBeInTheDocument()

        expect(
            screen.getByText('Environment: Lab')
        ).toBeInTheDocument()

        expect(
            screen.getByText(
                'Data classification: Unknown (not recorded)',
            ),
        ).toBeInTheDocument()

        expect(
            screen.getByText(
                'Discovery source: Built-in demo fixture',
            ),
        ).toBeInTheDocument()

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
                    identity_mode: 'unconfigured',
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

    it('rejects an asset ID begining with a hyphen', async () => {
        fetchMock.mockResolvedValue(
            jsonResponse([{ ...asset, asset_id: '-lab-api' }]),
        )

        render(<InventoryPanel />)
        loadInventory()

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'Server returned an invalid inventory response.',
        )

        expect(
            screen.queryByRole('heading', { name: asset.name }),
        ).not.toBeInTheDocument()
    })

    it('displays a recorded owner and environment', async () => {
        fetchMock.mockResolvedValue(
            jsonResponse([
                {
                    ...asset,
                    owner_team: 'Demo Platform Team',
                    environment: 'production',
                },
            ]),
        )

        render(<InventoryPanel />)
        loadInventory()

        expect(
            await screen.findByText('Owner team: Demo Platform Team'),
        ).toBeInTheDocument()

        expect(
            screen.getByText('Environment: Production'),
        ).toBeInTheDocument()

        expect(
            screen.getByText('Verification: unverified'),
        ).toBeInTheDocument()
    })

    it('displays an unknown environment explicitly', async () => {
        fetchMock.mockResolvedValue(
            jsonResponse([{ ...asset, environment: 'unknown' }]),
        )

        render(<InventoryPanel />)
        loadInventory()

        expect(
            await screen.findByText('Environment: Unknown'),
        ).toBeInTheDocument()
    })

    it.each([
        { owner_team: '' },
        { owner_team: '   ' },
        { owner_team: 42 },
        { owner_team: 'x'.repeat(121) },
        { environment: 'internet' },
        { environment: null },
        { owner_team: undefined },
        { environment: undefined },
        { data_classification: '' },
        { data_classification: 'secret' },
        { data_classification: null },
        { data_classification: 42 },
        { data_classification: undefined },
        { discovery_source: '' },
        { discovery_source: 'network_scan' },
        { discovery_source: null },
        { discovery_source: 42 },
        { discovery_source: undefined },
    ])('rejects invalid metadata: %j', async (overrides) => {
        fetchMock.mockResolvedValue(
            jsonResponse([{ ...asset, ...overrides }]),
        )

        render(<InventoryPanel />)
        loadInventory()

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'Server returned an invalid inventory response.',
        )

        expect(
            screen.queryByRole('heading', { name: asset.name }),
        ).not.toBeInTheDocument()
    })

    it.each([
        ['public', 'Public'],
        ['internal', 'Internal'],
        ['confidential', 'Confidential'],
        ['restricted', 'Restricted'],
    ])(
        'displays classification %s without implying verification',
        async (classification, label) => {
            fetchMock.mockResolvedValue(
                jsonResponse([
                    { ...asset, data_classification: classification },
                ]),
            )
            render(<InventoryPanel />)
            loadInventory()

            expect(
                await screen.findByText(
                    `Data classification: ${label}`,
                ),
            ).toBeInTheDocument()

            expect(
                screen.getByText('Synthetic demo record'),
            ).toBeInTheDocument()

            expect(
                screen.getByText('Verification: unverified'),
            ).toBeInTheDocument()
        },
    )

    it('displays an unknown discovery source explicitly', async () =>{
        fetchMock.mockResolvedValue(
            jsonResponse([{ ...asset, discovery_source: 'unknown' }]),
        )

        render(<InventoryPanel />)
        loadInventory()

        expect(
            await screen.findByText(
                'Discovery source: Unknown (not recorded)',
            ),
        ).toBeInTheDocument()

        expect(
            screen.getByText('Synthetic demo record'),
        ).toBeInTheDocument()

        expect(
            screen.getByText('Verification: unverified'),
        ).toBeInTheDocument()
    })

    it('displays five demo asset categories using one read request', async () => {
        const demoAssets: SecurityAsset[] = [
            asset,
            {
                ...asset,
                asset_id: 'demo-web-server',
                name: 'Demo web sever',
                asset_type: 'server',
                owner_team: 'Demo Infrastructure Team',
            },
            {
                ...asset,
                asset_id: 'demo-php-app',
                name: 'Demo PHP application',
                asset_type: 'application',
                owner_team: 'Demo Application Team',
            },
            {
                ...asset,
                asset_id: 'demo-container',
                name: 'Demo container',
                asset_type: 'container',
                owner_team: 'Demo Infrastructure Team',
            },
            {
                ...asset,
                asset_id: 'demo-ai-agent',
                name: 'Demo AI agent',
                asset_type: 'ai_agent',
                owner_team: 'Demo AI Team',
            },
        ]

        fetchMock.mockResolvedValueOnce(jsonResponse(demoAssets))

        render(<InventoryPanel />)
        loadInventory()

        expect(
            await screen.findByText('Records loaded: 5.'),
        ).toBeInTheDocument()

        expect(screen.getAllByRole('listitem')).toHaveLength(5)

        for (const record of demoAssets) {
            expect(
                screen.getByRole('heading', {name: record.name }),
            ).toBeInTheDocument()
        }

        for (const label of [
            'API',
            'Server',
            'Application',
            'Container',
            'AI agent'
        ]) {
            expect(
                screen.getByText(`Type: ${label}`),
            ).toBeInTheDocument()
        }

        expect(
            screen.getAllByText('Synthetic demo record'),
        ).toHaveLength(5)

        expect(
            screen.getAllByText('Verification: unverified')
        )

        expect(
            screen.getAllByText('Discovery source: Built-in demo fixture'),
        ).toHaveLength(5)

        expect(fetchMock).toHaveBeenCalledTimes(1)
        expect(fetchMock).toHaveBeenCalledWith(
            '/api/assets',
            expect.objectContaining({
                headers: { Accept: 'application/json' },
            }),
        )

        for (const [, options] of fetchMock.mock.calls) {
            expect(options?.method ?? 'GET').toBe('GET')
        }
    })
})