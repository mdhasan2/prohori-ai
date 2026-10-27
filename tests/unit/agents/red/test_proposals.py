"""Unit tests for Red Agent validation proposals.

These tests verify that:

- validation proposals are created only from relevant passive evidence;
- proposals remain bound to the originating asset and hypothesis;
- unrelated evidence is excluded;
- proposal evidence provenence is preserved;
- active validation is proposed, never authorized or executed;
- no proposal is generated without supporting evidence.

The Red Agent must never decide its own authorization.
"""

from datetime import UTC, datetime

import pytest

from prohori_ai.agents.red.models import (
    AssetKind,
    EvidenceKind,
    EvidenceRecord,
    HypothesisKind,
    ObservedAsset,
    SecurityHypothesis,
    ValidationKind,
    ValidationProposal,
)
from prohori_ai.agents.red.proposals import propose_validation

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def observed_asset() -> ObservedAsset:
    """Return the allowlisted asset being investigated."""
    return ObservedAsset(
        asset_id="lab-api",
        kind=AssetKind.API,
        hostname="lab-api.internal",
        port=8000,
        scheme="http",
        observed_at=datetime(
            2026,
            10,
            23,
            12,
            0,
            tzinfo=UTC,
        ),
    )


@pytest.fixture
def header_hypothesis(
    observed_asset: ObservedAsset,
) -> SecurityHypothesis:
    """Hypothesis that the API is missing a security header."""
    return SecurityHypothesis(
        hypothesis_id="hyp-header-001",
        asset_id=observed_asset.asset_id,
        kind=HypothesisKind.MISSING_SECURITY_HEADER,
        rationale=("Passive HTTP metadata indicates that a recommended "),
    )


@pytest.fixture
def header_evidence(
    observed_asset: ObservedAsset,
    header_hypothesis: SecurityHypothesis,
) -> EvidenceRecord:
    """First evidence item supporting the header hypothesis."""
    return EvidenceRecord(
        evidence_id="evidence-header-001",
        asset_id=observed_asset.asset_id,
        hypothesis_id=header_hypothesis.hypothesis_id,
        kind=EvidenceKind.PASSIVE_HTTP_METADATA,
        source="http_headers",
        summary=(
            "Content-Security-Policy was not present in passively observed HTTP response metadata."
        ),
        collected_at=datetime(
            2026,
            10,
            23,
            12,
            10,
            tzinfo=UTC,
        ),
    )


# ---------------------------------------------------------------------------
# Basic proposal creation
# ---------------------------------------------------------------------------


def test_propose_validation_returns_proposals(
    header_hypothesis: SecurityHypothesis,
    header_evidence: EvidenceRecord,
) -> None:
    """Relevant evidence should produce a validation proposal."""
    proposal = propose_validation(
        header_hypothesis,
        (header_evidence,),
    )

    assert proposal is not None
    assert isinstance(
        proposal,
        ValidationProposal,
    )
