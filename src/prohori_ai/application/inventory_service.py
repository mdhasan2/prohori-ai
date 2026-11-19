"""Return explicit demo fixtures without contacting any target."""

from prohori_ai.application.demo_inventory import demo_assets
from prohori_ai.domain.security_asset import SecurityAsset


class InventoryService:
    """Return the explicit demo fixture without contacting any target."""

    def list_assets(self) -> tuple[SecurityAsset, ...]:
        return demo_assets()
