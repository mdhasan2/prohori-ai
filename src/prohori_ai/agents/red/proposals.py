from uuid import uuid4

from prohori_ai.agents.red.models import (
    EvidenceRecord,
    HypothesisKind,
    SecurityHypothesis,
    ValidationKind,
    ValidationProposal,
)


def propose_validation(
    hypothesis: SecurityHypothesis,
    evidence: tuple[EvidenceRecord, ...],
) -> ValidationProposal | None:
    matching = tuple(
        item
        for item in evidence
        if (item.hypothesis_id == hypothesis.hypothesis_id and item.asset_id == hypothesis.asset_id)
    )

    if not matching:
        return None

    validation_kind: ValidationKind

    if hypothesis.kind is HypothesisKind.MISSING_SECURITY_HEADER:
        validation_kind = ValidationKind.CHECK_RESPONSE_HEADER

    elif hypothesis.kind is HypothesisKind.PATH_TRAVERSAL:
        validation_kind = ValidationKind.CHECK_PATH_TRAVERSAL

    else:
        return None

    return ValidationProposal(
        proposal_id=str(uuid4()),
        asset_id=hypothesis.asset_id,
        hypothesis_id=hypothesis.hypothesis_id,
        validation_kind=validation_kind,
        requested_capability="active_validation",
        rationale=(
            "Passive evidence supports controlled validation against the same allowlisted asset."
        ),
        evidence_ids=tuple(item.evidence_id for item in matching),
    )
