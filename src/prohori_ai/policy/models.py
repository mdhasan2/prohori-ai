from datetime import datetime
from enum import StrEnum
from typing import Self

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


class TargetRuleKind(StrEnum):
    EXACT_HOST = "exact_host"
    SUBDOMAIN = "subdomain"
    CIDR = "cidr"


class TargetRule(BaseModel):
    """One explicityly authorized target boundary."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    kind: TargetRuleKind
    value: str = Field(min_length=1)


class ScopePolicy(BaseModel):
    """Explicit authorization boundary for an investigation."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    allowed_targets: tuple[TargetRule, ...] = ()


class AuthorizationRequest(BaseModel):
    """Proposed tool action submitted to the policy engine."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    tool_name: str = Field(min_length=1)
    target: str | None = None
    human_approval_granted: bool = False


class PolicyDecisionCode(StrEnum):
    ALLOWED = "allowed"

    EMERGENCCY_STOP_ACTIVE = "emergency_stop_active"
    UNKNOWN_TOOL = "unknown_tool"
    DESTRUCTIVE_CAPABILITY = "destructive_capability"
    TARGET_REQUIRED = "target_required"
    TARGET_OUT_OF_SCOPE = "target_out_of_scope"
    APPROVAL_REQUIRED = "approval_required"
    BUDGET_EXHAUSTED = "budget_exhausted"


class PolicyDecision(BaseModel):
    """Immutable authorization result produced by the policy engine."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    allowed: bool
    code: PolicyDecisionCode
    explanation: str

    tool_name: str
    target: str | None

    capability_class: CapabilityClass | None = None
    budget_cost: int = 0
    budget_remaining: int


class ActionBudget(BaseModel):
    """Snapshot of an investigation's allowed action consumption."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    limit: int = Field(ge=0)
    consumed: int = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_consumption(self) -> Self:
        """Prevent impossible budget states."""

        if self.consumed > self.limit:
            raise ValueError("Consumed actions cannot exceed the budget limit")

        return self

    @property
    def remaining(self) -> int:
        return self.limit - self.consumed

    def can_afford(self, cost: int) -> bool:
        if cost < 1:
            raise ValueError("Budget cost must be positive")

        return self.remaining >= cost

    def consume(self, cost: int) -> Self:
        """Return a new budget snapshot with cost consumed."""

        if not self.can_afford(cost):
            raise ValueError("Action budget exhausted")

        return type(self)(
            limit=self.limit,
            consumed=self.consumed + cost,
        )


class EmergencyStop(BaseModel):
    """Operator-controlled global execution stop."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    enabled: bool = False
    reason: str | None = None

    def require_reason_when_enabled(self) -> Self:
        if self.enabled and not self.reason:
            raise ValueError("An enabled emergency stop requires a reason")

        return self
