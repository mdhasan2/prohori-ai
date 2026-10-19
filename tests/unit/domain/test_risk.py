"""Tests for deterministic risk assessment."""

import pytest
from pydantic import ValidationError

from prohori_ai.domain.risk import RiskAssessment, RiskSeverity


@pytest.mark.parametrize(
    ("likelihood", "impact", "expected_score", "severity"),
    [
        (1, 1, 1, RiskSeverity.INFORMATIONAL),
        (2, 2, 4, RiskSeverity.LOW),
        (3, 3, 9, RiskSeverity.MEDIUM),
        (4, 4, 16, RiskSeverity.HIGH),
        (5, 5, 25, RiskSeverity.CRITICAL),
    ],
)
def test_risk_severity(
    likelihood: int,
    impact: int,
    expected_score: int,
    severity: RiskSeverity,
) -> None:
    risk = RiskAssessment(
        likelihood=likelihood,
        impact=impact,
        severity=severity,
    )

    assert risk.score == expected_score
    assert risk.severity is severity
