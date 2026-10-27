from typing import Any
from unittest.mock import AsyncMock

import pytest

from prohori_ai.agents.red.observation import observe_assets


@pytest.fixture
def empty_asset_context() -> AsyncMock:
    """Return an asset-context client containing no assets"""
    context = AsyncMock()
    context.observe_assets = AsyncMock(
        return_value=(),
    )

    return context


# @pytest.mark.asyncio
# async def test_observe_assets_returns_context_assets(fake_asset_context):
#     assets = await observe_assets(fake_asset_context)

#     assert len(assets) == 1
#     assert assets[0].asset_id == "lab-api"


@pytest.mark.asyncio
async def test_observe_assets_handles_empty_scope(
    empty_asset_context: AsyncMock,
) -> None:
    assets = await observe_assets(empty_asset_context)

    assert assets == ()
