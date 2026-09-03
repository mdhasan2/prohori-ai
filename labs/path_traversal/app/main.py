"""Intentionally vulnerable local path traversal lab."""

from enum import StrEnum

from fastapi import FastAPI


class LabMode(StrEnum):
    """Supported lab execution modes."""

    VULNERABLE = "vulnerable"


app = FastAPI()


@app.get("/health")
def health() -> dict[str, str]:
    """Report whether the lab service is running."""
    return {"status": "healthy"}