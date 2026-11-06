"""Tests for the AuditEvent domain model."""

from datetime import UTC, datetime, timezone

import pytest
from pydantic import ValidationError

from prohori_ai.domain.audit import AuditEvent

NOW = datetime.now(UTC)


@pytest.fixture
def audit_event() -> AuditEvent:
    return AuditEvent(
        actor="human:human-001",
        action="validation.approved",
        subject="validation_proposal:proposal-001",
        correlation_id="corr-001",
        details={
            "investigation_id": "inv-001",
            "asset_id": "lab-api",
            "capability": "validate_path_traversal",
            "decision": "approved",
        },
    )


def test_create_audit_event(
    audit_event: AuditEvent,
) -> None:
    assert audit_event.actor == "human:human-001"
    assert audit_event.action == "validation.approved"
    assert audit_event.subject == "validation_proposal:proposal-001"
    assert audit_event.correlation_id == "corr-001"
    assert audit_event.details["asset_id"] == "lab-api"
    assert audit_event.details["decision"] == "approved"
