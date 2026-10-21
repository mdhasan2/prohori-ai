from prohori_ai.policy.models import (
    ScopePolicy,
    TargetRule,
    TargetRuleKind,
)
from prohori_ai.policy.targeting import target_is_authorized


def test_exact_authorized_target_is_accepted() -> None:
    scope = ScopePolicy(
        allowed_targets=(
            TargetRule(
                kind=TargetRuleKind.EXACT_HOST,
                value="lab.example.internal",
            ),
        )
    )

    assert target_is_authorized(
        "https://lab.example.internal:8443/test",
        scope,
    )
