
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import Field

from prohori_ai.domain.common import TimestampedModel, new_id, utc_now
from prohori_ai.domain.risk import RiskAssessment


class FindingStatus(StrEnum):
    CANDIDATE = "candidate"
    CONFIRMED = "confiremed"
    REJECTED = "rejected"
    ACCEPTED_RISK = "accepted_risk"
    REMEDIATED = "remediated"

class Finding(TimestampedModel):
    id: UUID = Field(default_factory=new_id)
    investigation_id: UUID

    title: str = Field(
        min_length=1,
        max_length=300,
    )

    description: str = Field(
        min_length=1,
        max_length=10_000,
    )

    status: FindingStatus = FindingStatus.CANDIDATE

    evidence_ids: tuple[UUID, ...] = ()

    risk: RiskAssessment | None = None

    created_at: datetime = Field(
        default_factory=utc_now
    )
