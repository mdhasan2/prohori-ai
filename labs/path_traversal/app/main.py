"""Intentionally vulnerable local path traversal lab."""

from enum import StrEnum

class LabMode(StrEnum):
    """Supported lab execution modes."""
    VULNERABLE = "vulnerable"