"""Core inventory contracts, independent of execution infrastructure."""

from enum import StrEnum
from typing import Literal

from pydantic import Field

from prohori_ai.domain.common import DomainModel


class AssetType(StrEnum):
    SERVER = "server"
    APPLICATION = "application"
    API = "api"
    CONTAINER = "container"
    KUBERNETES_WORKLOAD = "kubernetes_workload"
    CLOUD_RESOURCE = "cloud_resource"
    AI_AGENT = "ai_agent"


class AssetEnvironment(StrEnum):
    UNKNOWN = "unknown"
    LAB = "lab"
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class SecurityAsset(DomainModel):
    """An inventory record, not an execution authorization."""

    asset_id: str = Field(
        min_length=1,
        max_length=64,
        pattern=r"^[a-z0-9][a-z0-9_-]*$",
    )
    name: str = Field(min_length=1, max_length=200)
    asset_type: AssetType
    owner_team: str | None = Field(
        default=None,
        min_length=1,
        max_length=120,
    )
    environment: AssetEnvironment = AssetEnvironment.UNKNOWN

    # This first implementaion accepts synthetic, unverified records only.
    record_origin: Literal["synthetic"] = "synthetic"
    verification_state: Literal["unverified"] = "unverified"
