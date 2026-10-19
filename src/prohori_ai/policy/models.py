from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, model_validator


class CapabilityClass(StrEnum):
    """Security impact classification of a tool capability."""

    PASSIVE = "passive"
    ACTIVE = "active"
    DESTRUCTIVE = "destructive"


class ApprovalRequirement(StrEnum):
    """Human-approval requirement associated with a capability."""

    NONE = "none"
    HUMAN = "human"
    PERMANENT_DENY = "permanent_deny"


class ToolCapability(BaseModel):
    """Trusted policy metadata describing a callable tool."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(min_length=1)
    capability_class: CapabilityClass
    requires_target: bool = True
    budget_cost: int = Field(default=1, ge=1)

    @property
    def approval_requirement(self) -> ApprovalRequirement:
        """Derive approval requirements from capability classification."""

        if self.capability_class is CapabilityClass.DESTRUCTIVE:
            return ApprovalRequirement.PERMANENT_DENY

        if self.capability_class is CapabilityClass.ACTIVE:
            return ApprovalRequirement.HUMAN

        return ApprovalRequirement.NONE


class TagetRuleKind(StrEnum):
    EXACT_HOST = "exact_host"
    SUBDOMIN = "subdomain"
    CIDR = "cidr"


class TargetRule(BaseModel):
    """One explicityly authorized target boundary."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    kind: TagetRuleKind
    value: str = Field(min_length=1)


# class EmergencyStop(BaseModel):
#     """Operator-controlled global execution stop."""

#     @model
