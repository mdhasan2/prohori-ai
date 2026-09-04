"""Intentionally vulnerable local path traversal lab."""

from enum import StrEnum

from fastapi import FastAPI


class LabMode(StrEnum):
    """Supported lab execution modes."""

    VULNERABLE = "vulnerable"


#app = FastAPI()


# @app.get("/health")
# def health() -> dict[str, str]:
#     """Report whether the lab service is running."""
#     return {"status": "healthy"}

# @app.get("/")
# def root() -> dict[str, str]:
#     """Describe the local lab service."""
#     return {
#         "name": "Prohori AI Path Traversal Lab"
#     }

def create_app() -> FastAPI:
    """Create the lab application for the requested security state."""

    app = FastAPI(
        title="Prohori AI Path Traversal Lab",
        version="1.0.0",
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        """Report whether the lab service is running."""
        print("You are here")
        return {"status": "healthy"}

    return app


app = create_app()