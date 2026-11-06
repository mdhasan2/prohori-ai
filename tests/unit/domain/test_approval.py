"""Tests for human approval records."""

from datetime import UTC, datetime, timedelta, timezone
from uuid import UUID

import pytest

from prohori_ai.domain.approval import ApprovalRecord

APPROVAL_ID = UUID("00000000-0000-0000-0000-000000000001")

APPROVAL_ID = "approval-001"


@pytest.fixture
def valid_approval() -> ApprovalRecord:
    now = datetime.now(UTC)

    return ApprovalRecord(
        approval_id=APPROVAL_ID,
        action="validate_path_traversal",
        decision="approved",
        approver="human-001",
        scope="lab-api",
        expires_at=now + timedelta(minutes=15),
    )


def test_create_approval(
    valid_approval: ApprovalRecord,
) -> None:
    assert valid_approval.decision == "approved"
    assert valid_approval.scope == "lab-api"
