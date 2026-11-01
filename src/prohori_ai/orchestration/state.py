from typing import TypedDict


class SupervisorState(TypedDict):
    """Checkpointable state shared between supervisor nordes."""

    investigation_id: str
    asset_id: str

    current_stage: str

    observation_id: str | None
    finding_id: str | None

    validation_approval_id: str | None
    remidiation_approval_id: str | None

    validation_succeeded: bool | None
    remidiation_succeeded: bool | None
    verification_succeeded: bool | None

    failure_code: str | None
    failure_reason: str | None
