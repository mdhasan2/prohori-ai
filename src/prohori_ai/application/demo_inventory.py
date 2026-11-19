"""Explicit synthetic records for the local inventory demonstration."""

from prohori_ai.domain.security_asset import (
    AssetEnvironment,
    AssetType,
    DataClassification,
    DiscoverySource,
    SecurityAsset,
)


def _demo_asset(
    asset_id: str,
    name: str,
    asset_type: AssetType,
    owner_team: str | None,
) -> SecurityAsset:
    return SecurityAsset(
        asset_id=asset_id,
        name=name,
        asset_type=asset_type,
        owner_team=owner_team,
        environment=AssetEnvironment.LAB,
        data_classification=DataClassification.UNKNOWN,
        discovery_source=DiscoverySource.DEMO_FIXTURE,
        record_origin="synthetic",
        verification_state="unverified",
    )


def demo_assets() -> tuple[SecurityAsset, ...]:
    """Build the demo inventory without discovery or target access."""
    return (
        _demo_asset(
            "lab-api",
            "Path-traversal lab API",
            AssetType.API,
            None,
        ),
        _demo_asset(
            "demo-web-server",
            "Demo web server",
            AssetType.SERVER,
            "Demo Infrastructure Team",
        ),
        _demo_asset(
            "demo-php-app",
            "Demo PHP application",
            AssetType.APPLICATION,
            "Demo Application Team",
        ),
        _demo_asset(
            "demo-container",
            "Demo container",
            AssetType.CONTAINER,
            "Demo Infrastructure Team",
        ),
        _demo_asset(
            "demo-ai-agent",
            "Demo AI agent",
            AssetType.AI_AGENT,
            "Demo AI Team",
        ),
    )
