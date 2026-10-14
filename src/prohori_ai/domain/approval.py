from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict


class ApprovalRecord(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    approval_id: str
    action: str
    decision: Literal["approved", "rejected"]
    approver: str
    scope: str
    expires_at: datetime
