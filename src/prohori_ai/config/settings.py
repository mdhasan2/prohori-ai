"""Validated ProhoriAI runtime configuration."""

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

EnvironmentName = Literal["development", "test", "production"]
LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


class Settings(BaseSettings):
    """Configuration loaded from environment variables or a local .env file."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="PROHORIAI_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    environment: EnvironmentName = "development"
    require_human_approval: bool = True
    log_level: LogLevel = "INFO"
    project_name: str = Field(default="ProhoriAI", min_length=1)


@lru_cache
def get_settings() -> Settings:
    """Return a cached, validated settings instance."""
    return Settings()
