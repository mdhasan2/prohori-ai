from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID

from pydantic import Field, field_validator

from prohori_ai.domain.common import DomainModel, TimestampedModel, new_id, utc_now


class EvidenceSourceType(StrEnum):
    TOOL = "tool"
    AGENT = "agent"
    HUMAN = "human"
    SYSTEM = "system"


class EvidenceProvenance(DomainModel):
    source_type: EvidenceSourceType
    source_name: str = Field(min_length=1, max_length=200)
    source_version: str | None = Field(
        default=None,
        max_length=100,
    )
    captured_at: datetime
    locator: str = Field(min_length=1, max_length=2_000)

    @field_validator("captured_at")
    @classmethod
    def require_timezone(cls, value: datetime) -> datetime:
        if value.tzinfo is None or value.utcoffset() is None:
            raise ValueError("captured_at must be timezone-aware")

        return value.astimezone(UTC)


class Evidence(TimestampedModel):
    id: UUID = Field(default_factory=new_id)
    investigation_id: UUID

    summary: str = Field(
        min_length=1,
        max_length=4_000,
    )

    provenance: EvidenceProvenance

    sha256: str | None = None

    created_at: datetime = Field(default_factory=utc_now)

    @field_validator("sha256")
    @classmethod
    def validate_sha256(
        cls,
        value: str | None,
    ) -> str | None:
        if value is None:
            return None

        normalized = value.lower()

        if len(normalized) != 64:
            raise ValueError("sha256 must contain 64 hexadecimal characters")

        try:
            int(normalized, 16)
        except ValueError as exc:
            raise ValueError("sha256 must be hexadecimal") from exc

        return normalized
