from prohori_ai.agents.red.models import ObservedAsset
from prohori_ai.agents.red.ports import AssetObservationPort


async def observe_assets(
    asset_context: AssetObservationPort,
) -> tuple[ObservedAsset, ...]:
    return await asset_context.observe_assets()
