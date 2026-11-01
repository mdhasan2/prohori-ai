# class RedAgent
from prohori_ai.agents.red.models import (
    EvidenceRecord,
    ObservedAsset,
    SecurityHypothesis,
    ValidationProposal,
)
from prohori_ai.agents.red.ports import (
    AssetObservationPort,
    HypothesisGenerator,
    PassiveEvidencePort,
)
from prohori_ai.agents.red.proposals import propose_validation


class RedAgent:
    def __init__(
        self,
        *,
        asset_observer: AssetObservationPort,
        hypthesis_generator: HypothesisGenerator,
        passive_evidence: PassiveEvidencePort,
    ) -> None:
        self._asset_observer = asset_observer
        self._hypothesis_generator = hypthesis_generator
        self._passive_evidence = passive_evidence

    async def observe(
        self,
    ) -> tuple[ObservedAsset, ...]:
        return await self._asset_observer.observe_assets()

    async def hypothesize(
        self,
        asset: ObservedAsset,
    ) -> tuple[SecurityHypothesis, ...]:
        return await self._hypothesis_generator.generate(asset)

    async def collect_evidence(
        self,
        hypothesis: SecurityHypothesis,
    ) -> tuple[EvidenceRecord, ...]:
        return await self._passive_evidence.collect(
            asset_id=hypothesis.asset_id,
            hypothesis=hypothesis,
        )

    def propose(
        self,
        hypothesis: SecurityHypothesis,
        evidence: tuple[EvidenceRecord, ...],
    ) -> ValidationProposal | None:
        return propose_validation(
            hypothesis,
            evidence,
        )
