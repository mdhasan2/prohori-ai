from typing import Protocol

from prohori_ai.agents.red.models import (
    EvidenceRecord,
    HypothesisKind,
    ObservedAsset,
    SecurityHypothesis,
)


class AssetObservationPort(Protocol):
    async def observe_assets(self) -> tuple[ObservedAsset, ...]:
        """Return only assets exposed by the trusted asset-context service."""
        ...


class HypothesisGenerator(Protocol):
    async def generate(
        self,
        asset: ObservedAsset,
    ) -> tuple[SecurityHypothesis, ...]: ...


class PassiveEvidencePort(Protocol):
    async def collect(
        self,
        *,
        asset_id: str,
        hypothesis: SecurityHypothesis,
    ) -> tuple[EvidenceRecord, ...]: ...
