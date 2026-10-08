"""Allowlisted asset registry exposed through MCP."""

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True, slots=True)
class Asset:
    """A security-testing asset controlled by Prohori AI."""

    asset_id: str
    name: str
    base_url: str
    environment: str
    allowed_checks: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class AssetRelationship:
    """A relationship between two allowlisted assets."""

    source_asset_id: str
    relationship: str
    target_asset_id: str


class AssetRegistry:
    """Immutable allowlist of assets available to security tooling."""

    def __init__(
        self,
        assets: tuple[Asset, ...],
        relationships: tuple[AssetRelationship, ...],
    ) -> None:
        self._assets: Mapping[str, Asset] = MappingProxyType(
            {asset.asset_id: asset for asset in assets}
        )
        self._relationships = relationships

    def list_assets(self) -> tuple[Asset, ...]:
        """Return every allowlisted asset."""

        return tuple(self._assets.values())
