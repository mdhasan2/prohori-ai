from prohori_ai.agents.red.models import (
    EvidenceRecord,
    SecurityHypothesis,
)
from prohori_ai.agents.red.ports import PassiveEvidencePort


async def collect_passive_evidence(
    evidence_port: PassiveEvidencePort,
    *,
    asset_id: str,
    hypothesis: SecurityHypothesis,
) -> tuple[EvidenceRecord, ...]:
    if hypothesis.asset_id != asset_id:
        raise ValueError("Hypothesis asset does not match requested asset")

    return await evidence_port.collect(
        asset_id=asset_id,
        hypothesis=hypothesis,
    )
