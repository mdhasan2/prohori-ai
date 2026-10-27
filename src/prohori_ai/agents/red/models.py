from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class AssetKind(StrEnum):
    WEB_SERVICE = "web_service"
    API = "api"
    CONTAINER = "container"


class ObservedAsset(BaseModel):
    model_config = ConfigDict(frozen=True)

    asset_id: str
    kind: AssetKind
    hostname: str
    port: int = Field(ge=1, le=65535)
    scheme: str
    observed_at: datetime


# ---------------------------------------------------------------------------
# Hypotheses
# ---------------------------------------------------------------------------


class HypothesisKind(StrEnum):
    MISSING_SECURITY_HEADER = "missing_security_header"
    EXPOSED_DEBUG_METADATA = "exposed_debug_metadata"


class HypothesisStatus(StrEnum):
    PROPOSED = "proposed"
    SUPPORTED = "supported"
    REJECTED = "rejected"
    INCONCLUSIVE = "inconclusive"


class SecurityHypothesis(BaseModel):
    model_config = ConfigDict(frozen=True)

    hypothesis_id: str
    asset_id: str
    kind: HypothesisKind
    rationale: str = Field(min_length=1, max_length=500)
    status: HypothesisStatus = HypothesisStatus.PROPOSED


class EvidenceKind(StrEnum):
    PASSIVE_HTTP_METADATA = "passive_http_metadata"
    ACTIVE_VALIDATION = "active_validation"


class EvidenceRecord(BaseModel):
    model_config = ConfigDict(frozen=True)

    evidence_id: str
    asset_id: str
    hypothesis_id: str
    kind: EvidenceKind
    source: str
    summary: str
    collected_at: datetime


class ValidationKind(StrEnum):
    CHECK_RESPONSE_HEADER = "check_response_header"


class ValidationProposal(BaseModel):
    model_config = ConfigDict(frozen=True)

    proposal_id: str
    asset_id: str
    hypothesis_id: str
    validation_kind: ValidationKind

    requested_capability: str
    rationale: str = Field(min_length=1, max_length=500)

    evidence_ids: tuple[str, ...]
