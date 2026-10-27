from datetime import UTC, datetime
from unittest.mock import AsyncMock

import pytest

from prohori_ai.agents.red.evidence import collect_passive_evidence
from prohori_ai.agents.red.models import (
    AssetKind,
    EvidenceKind,
    EvidenceRecord,
    HypothesisKind,
    ObservedAsset,
    SecurityHypothesis,
)
from prohori_ai.agents.red.ports import PassiveEvidencePort

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def observed_asset() -> ObservedAsset:
    """Return an asset already exposed by trusted Asset Context."""
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
    """Return a hypothesis concerning a missing security header."""
    return SecurityHypothesis(
        hypothesis_id="hyp-header-001",
        asset_id=observed_asset.asset_id,
        kind=HypothesisKind.MISSING_SECURITY_HEADER,
        rationale=("The observed API may be missing recommend HTTP security headers."),
    )


@pytest.fixture
def header_evidence(
    observed_asset: ObservedAsset,
    header_hypothesis: SecurityHypothesis,
) -> EvidenceRecord:
    """Return passive evidence associated with the header hypothesis."""
    return EvidenceRecord(
        evidence_id="evidence-header-001",
        asset_id=observed_asset.asset_id,
        hypothesis_id=header_hypothesis.hypothesis_id,
        kind=EvidenceKind.PASSIVE_HTTP_METADATA,
        source="http_headers",
        summary=("HTTP response metadata does not include Content-Security-Policy."),
        collected_at=datetime(
            2026,
            10,
            23,
            12,
            10,
            tzinfo=UTC,
        ),
    )


@pytest.fixture
def second_header_evidence(
    observed_asset: ObservedAsset,
    header_evidence: SecurityHypothesis,
) -> EvidenceRecord:
    """Return another passive evidence record for the same hypothesis."""
    return EvidenceRecord(
        evidence_id="evidence-header-002",
        asset_id=observed_asset.asset_id,
        hypothesis_id=header_evidence.hypothesis_id,
        kind=EvidenceKind.PASSIVE_HTTP_METADATA,
        source="http_headers",
        summary=("HTTP response metadata includes X-Content-Type-Options."),
        collected_at=datetime(
            2026,
            10,
            23,
            12,
            11,
            tzinfo=UTC,
        ),
    )


@pytest.fixture
def passive_evidence_port(
    header_evidence: EvidenceRecord,
    second_header_evidence: EvidenceRecord,
) -> AsyncMock:
    """Return a mocked passive evidence provider."""
    port = AsyncMock(spec=PassiveEvidencePort)

    port.collect.return_value = (
        header_evidence,
        second_header_evidence,
    )

    return port


# ---------------------------------------------------------------------------
# Evidence binding
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_evidence_is_bound_to_hypothesis(
    passive_evidence_port: AsyncMock,
    observed_asset: ObservedAsset,
    header_hypothesis: SecurityHypothesis,
) -> None:
    """Every returned evidence item must belong to the requested hypothesis."""

    evidence = await collect_passive_evidence(
        passive_evidence_port,
        asset_id=observed_asset.asset_id,
        hypothesis=header_hypothesis,
    )

    assert evidence

    assert all(item.hypothesis_id == header_hypothesis.hypothesis_id for item in evidence)
