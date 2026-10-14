"""Tests for the Investigation domain model."""

from datetime import UTC, datetime, timezone

import pytest

from prohori_ai.domain.investigation import Investigation, InvestigationState


@pytest.fixture
def investigation() -> Investigation:
    """Create a valid new investigation"""
    return Investigation(
        name="Local Lab Security Assessment",
        objective="Assess an authorized local lab",
        state=InvestigationState.CREATED,
        created_at=datetime.now(UTC),
    )


def test_create_investigation(
    investigation: Investigation,
) -> None:
    assert investigation.id is not None
    assert investigation.name == "Local Lab Security Assessment"
    assert investigation.objective == "Assess an authorized local lab"
    assert investigation.state is InvestigationState.CREATED
    assert investigation.created_at.tzinfo is not None
