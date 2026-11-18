import { useState } from "react"
import { getSecurityAssets } from "../api/client"
import type {
    AssetEnvironment,
    DataClassification,
    DiscoverySource,
    SecurityAsset,
} from '../api/types'

const ENVIRONMENT_LABELS: Record<AssetEnvironment, string> = {
    unknown: 'Unknown',
    lab: 'Lab',
    development: 'Development',
    staging: 'Staging',
    production: 'Production',
}

const CLASSIFICATION_LABELS: Record<DataClassification, string> = {
    unknown: 'Unknown (not recorded)',
    public: 'Public',
    internal: 'Internal',
    confidential: 'Confidential',
    restricted: 'Restricted',
}

const DISCOVERY_SOURCE_LABELS: Record<DiscoverySource, string> = {
    unknown: 'Unknown (not recorded)',
    demo_fixture: 'Built-in demo fixture',
}

type InventoryState =
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'ready'; assets: SecurityAsset[] }
    | { status: 'error'; message: string }

export default function InventoryPanel() {
    const [state, setState] = useState<InventoryState>({
        status: 'idle',
    })

    async function loadInventory() {
        if (state.status === 'loading') return

        setState({ status: 'loading' })

        try {
            const assets = await getSecurityAssets()
            setState({ status: 'ready', assets})
        } catch (cause) {
            setState({
                status: 'error',
                message:
                    cause instanceof Error
                        ? cause.message
                        : 'Unable to load inventory.'
            })
        }
    }

    return (
        <section aria-labelledby="inventory-heading">
            <h2 id="inventory-heading">Asset inventory</h2>

            <p>
                Lab examples only. Loading inventory does not run security checks.
            </p>

            <button
                type="button"
                disabled={state.status === 'loading'}
                onClick={() => void loadInventory()}
            >
                Load lab inventory
            </button>

            {state.status === 'idle' && <p>Inventory not loaded.</p>}

            {state.status === 'loading' && (
                <p role="status">Loading inventory...</p>
            )}

            {state.status === 'error' && (
                <p role="alert">{state.message}</p>
            )}

            {state.status === 'ready' && (
                <>
                    <p role="status">
                        Records loaded: {state.assets.length}.
                    </p>

                    {state.assets.length === 0 ? (
                        <p>No asset records returned.</p>
                    ): (
                        <ul>
                            {state.assets.map((asset) => (
                                <li key={asset.asset_id}>
                                    <h3>{asset.name}</h3>
                                    <p>
                                        Asset ID: <code>{asset.asset_id}</code>
                                    </p>
                                    <p>Type: {asset.asset_type}</p>
                                    <p>
                                        Owner team: {' '}
                                        {asset.owner_team ?? 'Unknown (not recorded)'}
                                    </p>
                                    <p>
                                        Environment: {' '}
                                        {ENVIRONMENT_LABELS[asset.environment]}
                                    </p>
                                    <p>
                                        Data classification: {' '}
                                        {CLASSIFICATION_LABELS[
                                            asset.data_classification
                                        ]}
                                    </p>
                                    <p>
                                        Discovery source: {' '}
                                        {DISCOVERY_SOURCE_LABELS[
                                            asset.discovery_source
                                        ]}
                                    </p>
                                    <p>
                                        <strong>Synthetic demo record</strong>
                                    </p>
                                    <p>
                                        Verification: {asset.verification_state}
                                    </p>
                                </li>
                            ))}
                        </ul>
                    )}
                </>
            )}
        </section>
    )
}