from typing import Any

from pydantic import BaseModel, ConfigDict


class AuditEvent(BaseModel):
    model_config = ConfigDict(frozen=True, extra="forbid")

    actor: str
    action: str
    subject: str
    correlation_id: str
    details: dict[str, Any]
