"""Intentionally vulnerable local path traversal lab."""

import os
from enum import StrEnum
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

PUBLIC_DIR = Path("/lab/data/public")


class LabMode(StrEnum):
    """Supported lab execution modes."""

    VULNERABLE = "vulnerable"
    REMEDIATED = "remediated"


def read_file_vulnerable(file_path: str) -> str:
    """Read a file without enforcing the intended directory boundary."""

    candidate = PUBLIC_DIR / file_path
    print(candidate)

    try:
        content = candidate.read_text(encoding="utf-8")
        print(content)
        return content
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail="File not found",
        ) from exc


def read_file_remediated(file_path: str) -> str:
    """Read a file only if its resolved path remains inside PUBLIC_DIR."""
    pass


def create_app(mode: LabMode) -> FastAPI:
    """Create the lab application for the requested security state."""

    app = FastAPI(
        title="Prohori AI Path Traversal Lab",
        version="1.0.0",
    )

    @app.get("/")
    def root() -> dict[str, str]:
        """Describe the local lab service."""
        return {"name": "Prohori AI Path Traversal Lab"}

    @app.get("/health")
    def health() -> dict[str, str]:
        """Report whether the lab service is running."""
        return {
            "status": "healthy",
            "mode": mode.value,
        }

    @app.get(
        "/files/{file_path:path}",
        response_class=PlainTextResponse,
    )
    def get_file(file_path: str) -> str:
        if mode is LabMode.VULNERABLE:
            return read_file_vulnerable(file_path)
        return read_file_remediated(file_path)

    return app


def get_mode() -> LabMode:
    """Read and validate LAB_MODE"""

    raw_mode = os.getenv(
        "LAB_MODE",
        LabMode.REMEDIATED.value,
    )

    print(raw_mode)

    try:
        return LabMode(raw_mode)
    except ValueError as exc:
        raise RuntimeError(f"Unsupported LAB_M0DE: {raw_mode}") from exc


app = create_app(get_mode())
