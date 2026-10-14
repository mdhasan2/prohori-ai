"""Tests for the Finding domain model."""

from datetime import UTC, datetime, timezone
from uuid import UUID

import pytest
from pydantic import ValidationError

from prohori_ai.domain.finding import (
    Finding,
    FindingStatus,
)
from prohori_ai.domain.risk import RiskAssessment, RiskSeverity

NOW = datetime.now(UTC)
FINDING_ID = UUID("00000000-0000-0000-0000-000000000001")
INVESTIGATION_ID = UUID("00000000-0000-0000-0000-000000000002")


@pytest.fixture
def finding() -> Finding:
    """Create a valid unconfiremd finding."""
    return Finding(
        id=FINDING_ID,
        investigation_id=INVESTIGATION_ID,
        title="Potential Path Traversal",
        description="A file endpoint may allow directory traversal.",
        status=FindingStatus.CANDIDATE,
        evidence_ids=(),
        risk=RiskAssessment(
            likelihood=3,
            impact=4,
            severity=RiskSeverity.HIGH
        ),
        created_at=NOW,
    )


def test_create_finding(finding: Finding) -> None:
    assert finding.id == FINDING_ID
    assert finding.investigation_id == INVESTIGATION_ID
    assert finding.status is FindingStatus.CANDIDATE
    assert finding.risk.score == 12
    assert finding.risk.severity is RiskSeverity.HIGH
    assert finding.evidence_ids == ()

