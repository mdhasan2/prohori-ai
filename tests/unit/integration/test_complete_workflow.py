"""Integration tests for the deterministic Prohori-AI workflow.

Lifecycle:

    Observe
        -> Discover
        -> Request validation approval
        -> Validate
        -> Assess
        -> Request remediation approval
        -> Remediate
        -> Verify

Two independent approvals are required:

1. Active-validation approval
2. Remediation/modification approval

Approval #1 MUST NOT authorize approval #2
"""

# ---------------------------------------------------------------------------
# Test fixture
# ---------------------------------------------------------------------------
