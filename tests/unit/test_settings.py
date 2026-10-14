"""Tests for ProhoriAI environment configuration."""

import pytest

from prohori_ai.config.settings import Settings, get_settings


def test_settings_use_secure_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    """Human approval should be required unless explicitly configured otherwise."""
    monkeypatch.delenv("PROHORIAI_ENVIRONMENT", raising=False)

    # BaseSettings accepts _env_file at runtime, but mypy cannot see this
    # dynamically supplied constuctor parameter.
    settings = Settings(_env_file=None)  # type: ignore[call-arg]

    assert settings.environment == "development"
    assert settings.require_human_approval is True
    assert settings.log_level == "INFO"


def test_get_settings_returns_cached_instance() -> None:
    """Repeated configuration access should return the same validated instance."""
    get_settings.cache_clear()

    try:
        first = get_settings()
        second = get_settings()

        assert first is second
    finally:
        get_settings.cache_clear()
