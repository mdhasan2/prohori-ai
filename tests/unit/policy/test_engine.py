import pytest

from prohori_ai.policy.capabilities import CapabilityRegistry
from prohori_ai.policy.engine import PolicyEngine
from prohori_ai.policy.models import (
    ActionBudget,
    AuthorizationRequest,
    CapabilityClass,
    EmergencyStop,
    PolicyDecisionCode,
    ScopePolicy,
    TargetRule,
    TargetRuleKind,
    ToolCapability,
)


@pytest.fixture
def registry() -> CapabilityRegistry:
    return CapabilityRegistry(
        [
            ToolCapability(
                name="dns_lookup",
                capability_class=CapabilityClass.PASSIVE,
            ),
            ToolCapability(
                name="nmap_scan",
                capability_class=CapabilityClass.ACTIVE,
            ),
            ToolCapability(
                name="delete_resource",
                capability_class=CapabilityClass.DESTRUCTIVE,
            ),
        ]
    )


@pytest.fixture
def policy_engine(
    registry: CapabilityRegistry,
) -> PolicyEngine:
    return PolicyEngine(registry)


@pytest.fixture
def scope() -> ScopePolicy:
    return ScopePolicy(
        allowed_targets=(
            TargetRule(
                kind=TargetRuleKind.EXACT_HOST,
                value="lab.example.internal",
            ),
        )
    )


@pytest.fixture
def budget() -> ActionBudget:
    return ActionBudget(
        limit=10,
        consumed=0,
    )


@pytest.fixture
def emergency_stop_off() -> EmergencyStop:
    return EmergencyStop(enabled=False)


def test_authorized_target_is_accepted(
    policy_engine: PolicyEngine,
    scope: ScopePolicy,
    budget: ActionBudget,
    emergency_stop_off: EmergencyStop,
) -> None:
    decision = policy_engine.authorize(
        request=AuthorizationRequest(
            tool_name="dns_lookup",
            target="lab.example.internal",
        ),
        scope=scope,
        budget=budget,
        emergency_stop=emergency_stop_off,
    )

    assert decision.allowed
    assert decision.code is PolicyDecisionCode.ALLOWED
