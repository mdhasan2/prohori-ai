"""Intentionally vulnerable local path traversal lab."""

from enum import StrEnum

from fastapi import FastAPI


class LabMode(StrEnum):
    """Supported lab execution modes."""

    VULNERABLE = "vulnerable"


app = FastAPI()
