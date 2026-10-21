from ipaddress import AddressValueError, IPv4Address, IPv6Address, ip_address, ip_network
from urllib.parse import urlsplit

from prohori_ai.policy.models import ScopePolicy, TargetRule, TargetRuleKind


class InvalidTargetError(ValueError):
    """Raised when a requested target cannot be normalized."""


def normalize_target(target: str) -> str:
    """Normalize a URL, hostname, or IP into a policy-comparable host."""

    candidate = target.strip()

    if not candidate:
        raise InvalidTargetError("Target cannot be empty")

    try:
        return str(ip_address(candidate))
    except ValueError:
        pass

    if "://" in candidate:
        parsed = urlsplit(candidate)
    else:
        parsed = urlsplit(f"//{candidate}")

    hostname = parsed.hostname

    if hostname is None:
        raise InvalidTargetError(f"Unable to determine hostname from target: {target}")

    return hostname.rstrip(".").lower()


def target_matches_rule(
    target: str,
    rule: TargetRule,
) -> bool:
    """Return whether a target falls within one explicit scope rule."""

    normalized_target = normalize_target(target)

    if rule.kind is TargetRuleKind.EXACT_HOST:
        return normalized_target == rule.value.rstrip(".").lower()

    if rule.kind is TargetRuleKind.SUBDOMAIN:
        suffix = rule.value.rstrip(".").lower()
        return normalized_target != suffix and normalized_target.endswith(f".{suffix}")

    if rule.kind is TargetRuleKind.CIDR:
        try:
            target_ip = ip_address(normalized_target)
        except AddressValueError:
            return False

        network = ip_network(
            rule.value,
            strict=False,
        )
        return target_ip in network

    return False  # type: ignore[unreachable] # Defensive fail-closed fallback.


def target_is_authorized(
    target: str,
    scope: ScopePolicy,
) -> bool:
    """Return wheather any explicit scope rule authorizes the target."""

    try:
        return any(target_matches_rule(target, rule) for rule in scope.allowed_targets)
    except (InvalidTargetError, ValueError):
        return False
