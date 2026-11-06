from typing import cast
from unittest.mock import AsyncMock

import pytest

import prohori_ai.orchestration.nodes as nodes_module
from prohori_ai.orchestration.nodes import (
    discover_node,
    observe_node,
    request_validation_approval_node,
)
from prohori_ai.orchestration.state import SupervisorState

# ---------------------------------------------------------------------------
# Observe
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_observe_node_records_observation_id() -> None:
    state = cast(
        SupervisorState,
        {
            "investigation_id": "inv-001",
            "asset_id": "lab-api",
            "current_stage": "OBSERVERVING",
        },
    )

    result = await observe_node(state)

    assert result == {
        "current_stage": "OBSERVED",
        "observation_id": "observation:inv-001",
    }


# ---------------------------------------------------------------------------
# Discover
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_discover_node_records_discovery_outputs() -> None:
    state = cast(
        SupervisorState,
        {
            "investigation_id": "inv-001",
            "asset_id": "lab-api",
            "observation_id": "observation:inv-001",
            "current_stage": "OBSERVED",
        },
    )

    result = await discover_node(state)

    assert result == {
        "current_stage": "DISCOVERED",
        "finding_id": "finding:inv-001",
    }


@pytest.mark.asyncio
async def test_discover_node_rquires_observation() -> None:
    state = cast(
        SupervisorState,
        {
            "investigation_id": "inv-001",
            "asset_id": "lab-api",
            "observation_id": None,
            "current_stage": "OBSERVED",
        },
    )

    with pytest.raises(
        ValueError,
        match="Discovery requires an observation",
    ):
        await discover_node(state)


# ---------------------------------------------------------------------------
# Validation approval
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_validation_approval_inetrrupts_for_human_approval(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured_payload: dic[str, object] = {}

    def fake_interrupt(
        payload: dict[str, object],
    ) -> object:
        captured_payload.update(payload)

        return {
            "approved": True,
            "approval_id": "valication-approval-001",
        }

    monkeypatch.setattr(
        nodes_module,
        "interrupt",
        fake_interrupt,
    )

    state = cast(
        SupervisorState,
        {
            "investigation_id": "inv-001",
            "asset_id": "lab-api",
            "finding_id": "finding:inv-001",
            "current_stage": "DISCOVERED",
        },
    )

    result = await request_validation_approval_node(state)

    assert captured_payload == {
        "type": "approval_required",
        "action": "active_validation",
        "investigation_id": "inv-001",
        "asset_id": "lab-api",
        "finding_id": "finding:inv-001",
    }

    assert result == {
        "current_stage": "VALIDATION_APPROVED",
        "validation_approval_id": "valication-approval-001",
    }
