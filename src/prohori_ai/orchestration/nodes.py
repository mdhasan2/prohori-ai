from typing import TypedDict

from langgraph.types import interrupt

from prohori_ai.orchestration.state import SupervisorState


async def observe_node(state: SupervisorState) -> dict[str, object]:
    """Collect passive observations for the investigation"""

    # Replace with your Phase 6 workflow/application service.

    observation_id = f"observation:{state['investigation_id']}"

    return {
        "current_stage": "OBSERVED",
        "observation_id": observation_id,
    }


async def discover_node(state: SupervisorState) -> dict[str, object]:
    """Convert observation into candidate findings."""

    if state["observation_id"] is None:
        raise ValueError("Discovery requires an observation")

    finding_id = f"finding:{state['investigation_id']}"

    return {
        "current_stage": "DISCOVERED",
        "finding_id": finding_id,
    }


class ApprovalResponse(TypedDict):
    approved: bool
    approval_id: str | None


async def request_validation_approval_node(
    state: SupervisorState,
) -> dict[str, object]:
    """Pause before active security validation."""

    response = interrupt(
        {
            "type": "approval_required",
            "action": "active_validation",
            "investigation_id": state["investigation_id"],
            "asset_id": state["asset_id"],
            "finding_id": state["finding_id"],
        }
    )

    if not isinstance(response, dict):
        raise ValueError("Approval response must be an object")

    approved = response.get("approved")

    if approved is not True:
        return {
            "current_stage": "VALIDATION_REJECTED",
            "failure_code": "APPROVAL_REJECTED",
            "failure_reason": "Active validation was not approved.",
        }

    approval_id = response.get("approval_id")
    if not isinstance(approval_id, str):
        raise ValueError("Approved action requires approval_id")

    return {
        "current_stage": "VALIDATION_APPROVED",
        "validation_approval_id": approval_id,
    }


# async def validate_node(
#     state: SupervisorState
# ) -> dict[str, object]:

# async def assess_node(
#     state: SupervisorState
# ) -> dict[str, object]:

# async def remediate_node(
#     state: SupervisorState
# ) -> dict[str, object]:

# async def verify_node(
#     state: SupervisorState
# ) -> dict[str, object]:

# async def complete_node(
#     state: SupervisorState
# ) -> dict[str, object]:

# async def safe_failure_node(
#     state: SupervisorState
# ) -> dict[str, object]:
