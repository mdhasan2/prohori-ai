"""Local HTTP interface for the existing human-governed workflow."""

from pathlib import Path
from typing import Any, Literal
from uuid import UUID

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, ConfigDict, Field
from starlette.middleware.base import RequestResponseEndpoint
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import Response

from prohori_ai.application.local_workflow_service import (
    LocalWorkflowService,
    RunNotFoundError,
    WorkflowConflictError,
)


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class HealthResponse(StrictModel):
    status: Literal["ok"] = "ok"


class PendingApprovalResponse(StrictModel):
    gate: Literal["investigation", "validation"]
    binding: str
    asset_id: str
    operation: str
    proposal: dict[str, Any] | None


class RunResponse(StrictModel):
    run_id: UUID
    status: str
    pending_approval: PendingApprovalResponse | None
    state: dict[str, Any]
    stopped: bool


class DecisionRequest(StrictModel):
    expected_gate: Literal["investigation", "validation"]
    expected_binding: str = Field(min_length=1, max_length=4096)
    approved: bool = Field(strict=True)


class AuditEventResponse(StrictModel):
    id: int
    at: str
    action: str
    details: dict[str, Any]


class StopResponse(StrictModel):
    stopped: bool


class ErrorResponse(StrictModel):
    detail: str


ERROR_RESPONSES: dict[int | str, dict[str, Any]] = {
    404: {
        "model": ErrorResponse,
        "description": "The run does not exist.",
    },
    409: {
        "model": ErrorResponse,
        "description": "The operation conflicts with saved workflow state.",
    },
}


def create_app(directory: Path | None = None, allowed_origins: set[str] | None = None) -> FastAPI:
    service = LocalWorkflowService(directory)

    origins = (
        allowed_origins
        if allowed_origins is not None
        else {
            "http://127.0.0.1:5173",
            "http://localhost:5173",
            "http://127.0.0.1:8000",
        }
    )

    app = FastAPI(
        title="Prohori AI Local Operator API",
        version="0.1.0",
        description=(
            "Single-operator interface for the fixed local lab workflow. "
            "Approvals and tool authorizaiton are enforced by the backend."
        ),
    )

    @app.get(
        "/health",
        tags=["system"],
    )
    def health_check() -> dict[str, str]:
        """Report whether the API process is avialable."""
        return {"status": "healthy"}

    @app.middleware("http")
    async def protect_mutations(
        request: Request,
        call_next: RequestResponseEndpoint,
    ) -> Response:
        if request.method in {"POST", "PUT", "PATCH", "DELETE"}:
            origin = request.headers.get("origin")

            # Browser requests must originate from an explicitly allowed
            # local operator UI. Non-browser clients may omit Origin.

            if origin is not None and origin not in origins:
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Request origin is not allowed."},
                )

            content_type = request.headers.get("content-type", "")
            media_type = content_type.split(";", 1)[0].strip().lower()

            if media_type != "application/json":
                return JSONResponse(
                    status_code=415,
                    content={"detail": "Use application/json."},
                )

        return await call_next(request)

    @app.exception_handler(WorkflowConflictError)
    async def workflow_conflict_handler(
        request: Request,
        exc: WorkflowConflictError,
    ) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": str(exc)},
        )

    @app.get(
        "/api/health",
        response_model=HealthResponse,
        operation_id="getHealth",
    )
    def health() -> HealthResponse:
        return HealthResponse()

    @app.post(
        "/api/runs",
        response_model=RunResponse,
        status_code=201,
        responses=ERROR_RESPONSES,
        operation_id="createRun",
    )
    def create_run(body: StrictModel) -> RunResponse:
        # An empty JSON object is intentional: callers cannot choose
        # arbitrary targets, tools, or initial graph state.
        return RunResponse.model_validate(service.create_run())

    @app.get(
        "/api/runs/{run_id}",
        response_model=RunResponse,
        responses=ERROR_RESPONSES,
        operation_id="getRun",
    )
    def get_run(run_id: UUID) -> RunResponse:
        return RunResponse.model_validate(service.get_run(str(run_id)))

    @app.post(
        "/api/runs/{run_id}/decision",
        response_model=RunResponse,
        responses=ERROR_RESPONSES,
        operation_id="submitDecision",
    )
    def submit_decision(
        run_id: UUID,
        body: DecisionRequest,
    ) -> RunResponse:
        return RunResponse.model_validate(
            service.decide(
                run_id=str(run_id),
                expected_gate=body.expected_gate,
                expected_binding=body.expected_binding,
                approved=body.approved,
            )
        )

    @app.get(
        "/api/runs/{run_id}/audit",
        response_model=list[AuditEventResponse],
        responses=ERROR_RESPONSES,
        operation_id="getAudit",
    )
    def get_audit(run_id: UUID) -> list[AuditEventResponse]:
        return [
            AuditEventResponse.model_validate(event) for event in service.get_audit(str(run_id))
        ]

    @app.post(
        "/api/stop",
        response_model=StopResponse,
        operation_id="activateStop",
    )
    def activate_stop(body: StrictModel) -> StopResponse:
        return StopResponse.model_validate(service.activate_stop())

    return app


app = create_app()
