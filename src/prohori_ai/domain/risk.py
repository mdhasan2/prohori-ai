from enum import StrEnum

from pydantic import Field

from prohori_ai.domain.common import DomainModel


class RiskSeverity(StrEnum):
    INFORMATIONAL = "informational"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class RiskAssessment(DomainModel):
    likelihood: int = Field(ge=1, le=5)
    impact: int = Field(ge=1, le=5)
    severity: RiskSeverity

    @property
    def score(self) -> int:
        return self.likelihood * self.impact
