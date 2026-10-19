from ipaddress import (
    AddressValueError,
    IPv4Address,
    IPv6Address,
    ip_address,
    ip_network,
)
from urllib.parse import urlsplit


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
