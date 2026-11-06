"""Tests for evidence and provenance domain models."""

import hashlib
from datetime import UTC, datetime, timezone
from uuid import UUID

import pytest

from prohori_ai.domain.evidence import Evidence, EvidenceProvenance, EvidenceSourceType

NOW = datetime.now(UTC)
INVESTIGATION_ID = UUID("00000000-0000-0000-0000-000000000002")


@pytest.fixture
def provenance() -> EvidenceProvenance:
    return EvidenceProvenance(
        source_type=EvidenceSourceType.TOOL,
        source_name="security-testing-mcp",
        source_version="1.0.0",
        captured_at=NOW,
        locator="lab-api:/files/readme.txt",
    )


@pytest.fixture
def evidence(
    provenance: EvidenceProvenance,
) -> Evidence:
    digest = hashlib.sha256(b"sample evidence").hexdigest()

    return Evidence(
        investigation_id=INVESTIGATION_ID,
        summary="Local lab file observation",
        provenance=provenance,
        sha256=digest,
        created_at=NOW,
    )


def test_create_evidence(evidence: Evidence) -> None:
    assert isinstance(evidence.id, UUID)
    assert evidence.investigation_id == INVESTIGATION_ID
    assert evidence.sha256 is not None
    assert len(evidence.sha256) == 64


def test_evidence_has_valid_provenance(
    evidence: Evidence,
) -> None:
    assert evidence.provenance.source_name == "security-testing-mcp"
    assert evidence.provenance.locator == "lab-api:/files/readme.txt"
