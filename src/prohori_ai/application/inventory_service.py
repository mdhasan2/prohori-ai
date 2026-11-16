"""Read-only inventory service for the first console doemonstration."""

from prohori_ai.domain.security_asset import (
    AssetEnvironment,
    AssetType,
    DataClassification,
    SecurityAsset,
)


class InventoryService:
    """Return the explicit demo fixture without contacting any target."""

    def list_assets(self) -> tuple[SecurityAsset, ...]:
        return (
            SecurityAsset(
                asset_id="lab-api",
                name="Path-traversal lab API",
                asset_type=AssetType.API,
                owner_team=None,
                environment=AssetEnvironment.LAB,
                data_classification=DataClassification.UNKNOWN,
            ),
        )
