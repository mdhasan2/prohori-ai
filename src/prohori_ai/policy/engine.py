from prohori_ai.policy.capabilities import CapabilityRegistry
from prohori_ai.policy.models import (
    ActionBudget,
    AuthorizationRequest,
    EmergencyStop,
    PolicyDecision,
    PolicyDecisionCode,
    ScopePolicy,
    ToolCapability,
)
from prohori_ai.policy.targeting import target_is_authorized


def _deny(
    *,
    request: AuthorizationRequest,
    budget: ActionBudget,
    code: PolicyDecisionCode,
    explanation: str,
    capability: ToolCapability | None = None,
) -> PolicyDecision:
    return PolicyDecision(
        allowed=False,
        code=code,
        explanation=explanation,
        tool_name=request.tool_name,
        target=request.target,
        capability_class=(capability.capability_class if capability is not None else None),
        budget_cost=0,
        budget_remaining=budget.remaining,
    )


class PolicyEngine:
    """Evaluate proposed tool actions against trusted safety policy."""

    def __init__(
        self,
        capability_registry: CapabilityRegistry,
    ) -> None:
        self._capability_registry = capability_registry

    def authorize(
        self,
        *,
        request: AuthorizationRequest,
        scope: ScopePolicy,
        budget: ActionBudget,
        emergency_stop: EmergencyStop,
    ) -> PolicyDecision:
        """Return an authorization decision without executing anything."""

        if emergency_stop.enabled:
            return _deny(
                request=request,
                budget=budget,
                code=PolicyDecisionCode.EMERGENCCY_STOP_ACTIVE,
                explanation=(f"Emergency stop is active: {emergency_stop.reason}"),
            )

        capability = self._capability_registry.get(request.tool_name)

        if capability is None:
            return _deny(
                request=request,
                budget=budget,
                code=PolicyDecisionCode.UNKNOWN_TOOL,
                explanation=(f"Tool is not registered: {request.tool_name}"),
            )

        if capability.approval_requirement.value == "permanent_deny":
            return _deny(
                request=request,
                budget=budget,
                capability=capability,
                code=PolicyDecisionCode.DESTRUCTIVE_CAPABILITY,
                explanation=("Destructive capabilities are permanently denied"),
            )

        if capability.requires_target:
            if request.target is None:
                return _deny(
                    request=request,
                    budget=budget,
                    capability=capability,
                    code=PolicyDecisionCode.TARGET_REQUIRED,
                    explanation="Capability requires a target",
                )
            if not target_is_authorized(
                request.target,
                scope,
            ):
                return _deny(
                    request=request,
                    budget=budget,
                    capability=capability,
                    code=PolicyDecisionCode.TARGET_OUT_OF_SCOPE,
                    explanation=("Requested target is outside authorized scope"),
                )

        if capability.approval_requirement.value == "human" and not request.human_approval_granted:
            return _deny(
                request=request,
                budget=budget,
                capability=capability,
                code=PolicyDecisionCode.APPROVAL_REQUIRED,
                explanation=("Active capability requires human approval"),
            )

        if not budget.can_afford(capability.budget_cost):
            return _deny(
                request=request,
                budget=budget,
                capability=capability,
                code=PolicyDecisionCode.BUDGET_EXHAUSTED,
                explanation=("Action budget does not permit execution"),
            )

        return PolicyDecision(
            allowed=True,
            code=PolicyDecisionCode.ALLOWED,
            explanation="Policy permits executed",
            tool_name=request.tool_name,
            target=request.target,
            capability_class=capability.capability_class,
            budget_cost=capability.budget_cost,
            budget_remaining=budget.remaining,
        )
