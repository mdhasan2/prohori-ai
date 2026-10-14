
from datetime import datetime
from enum import StrEnum
from uuid import UUID

from pydantic import Field

from prohori_ai.domain.common import TimestampedModel, new_id, utc_now


class InvestigationState(StrEnum):
    CREATED = "created"
    SCOPED = "scoped"
    DISCOVERING = "discovering"
    AWAITING_APPROVAL = "awaiting_approval"
    VALIDATING = "validating"
    ANALYZING = "analyzing"
    FAILED = "failed"
    CANCELLED = "cancelled"


class Investigation(TimestampedModel):
    id: UUID = Field(default_factory=new_id)
    name: str = Field(min_length=1, max_length=200)
    objective: str = Field(min_length=1, max_length=2_000)
    state: InvestigationState = InvestigationState.CREATED
    created_at: datetime = Field(default_factory=utc_now)
