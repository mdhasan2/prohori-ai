from collections.abc import Iterable

from prohori_ai.policy.models import CapabilityClass, ToolCapability


class CapabilityRegistry:
    """Read-only lookup of explicityly registered capabilities."""

    def __init__(
        self,
        capabilities: Iterable[ToolCapability],
    ) -> None:
        registry: dict[str, ToolCapability] = {}

        for capability in capabilities:
            if capability.name in registry:
                raise ValueError(f"Duplicate capability: {capability.name}")

            registry[capability.name] = capability

        self._capabilities = registry

    def get(
        self,
        tool_name: str,
    ) -> ToolCapability | None:
        """Return capability metadata wehen explicitly registered."""

        return self._capabilities.get(tool_name)


DEFAULT_CAPABILITIES = CapabilityRegistry(
    [
        ToolCapability(
            name="dns_lookup",
            capability_class=CapabilityClass.PASSIVE,
            requires_target=True,
        ),
        ToolCapability(
            name="http_get",
            capability_class=CapabilityClass.PASSIVE,
            requires_target=True,
        ),
        ToolCapability(
            name="nmap_scan",
            capability_class=CapabilityClass.ACTIVE,
            requires_target=True,
            budget_cost=1,
        ),
        ToolCapability(
            name="nuclei_scan",
            capability_class=CapabilityClass.ACTIVE,
            requires_target=True,
            budget_cost=1,
        ),
        ToolCapability(
            name="delete_resource",
            capability_class=CapabilityClass.DESTRUCTIVE,
            requires_target=True,
        ),
    ]
)
