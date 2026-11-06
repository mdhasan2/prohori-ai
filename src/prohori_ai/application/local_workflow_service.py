"""Application service for the existing single-operator local workflow."""

import json
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from threading import Lock
from typing import Any, Literal, TypedDict
from uuid import UUID, uuid4

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command, StateSnapshot

from prohori_ai.application.local_workflow import Runtime, build_graph

Gate = Literal["investigation", "validation"]

# Shared across service instances in this Python process.
# Run the local API with one worker.
_WORKFLOW_LOCK = Lock()


class RunNotFoundError(Exception):
    """The requested run has no saved checkpoint."""


class WorkflowConflictError(Exception):
    """The requested operation conflicts with the saved workflow state."""


class PendingApproval(TypedDict):
    gate: Gate
    binding: str
    asset_id: str
    operation: str
    proposal: dict[str, Any] | None


class RunView(TypedDict):
    run_id: str
    status: str
    pending_approval: PendingApproval | None
    state: dict[str, Any]
    stopped: bool


class AuditEvent(TypedDict):
    id: int
    at: str
    action: str
    details: dict[str, Any]


def normalize_run_id(run_id: str) -> str:
    """Validate and normalize a UUID without using it as a file path."""
    return str(UUID(run_id))


class LocalWorkflowService:
    """Single-operator adapter around the existing CLI graph.

    CLI and API processes must not mutate the same run concurrently.
    The process lock does not coordinate separate operating-system processes.
    """

    def __init__(self, directory: Path | None = None) -> None:
        self.directory = directory or Path(".prohori-cli")

    @contextmanager
    def _session(
        self,
        run_id: str,
    ) -> Iterator[tuple[Runtime, Any, RunnableConfig]]:
        normalized = normalize_run_id(run_id)
        runtime = Runtime(self.directory, normalized)

        try:
            checkpoint_path = self.directory / "checkpoint.sqlite"

            with SqliteSaver.from_conn_string(str(checkpoint_path)) as saver:
                graph = build_graph(runtime, saver)
                config: RunnableConfig = {"configurable": {"thread_id": normalized}}
                yield runtime, graph, config
        finally:
            runtime.close()

    @staticmethod
    def _pending(snapshot: StateSnapshot) -> PendingApproval | None:
        interrupts = snapshot.interrupts

        if not interrupts:
            return None

        if len(interrupts) != 1:
            raise WorkflowConflictError("This interface supports exactly one pending approval.")

        value = interrupts[0].value

        if not isinstance(value, dict):
            raise WorkflowConflictError("Invalid saved approval request.")

        gate = value.get("gate")
        binding = value.get("binding")
        asset_id = value.get("asset_id")
        operation = value.get("operation")
        proposal = value.get("proposal")

        if gate not in ("investigation", "validation"):
            raise WorkflowConflictError("Unknown saved approval gate.")

        if (
            not isinstance(binding, str)
            or not binding
            or not isinstance(asset_id, str)
            or not isinstance(operation, str)
            or (proposal is not None and not isinstance(proposal, dict))
        ):
            raise WorkflowConflictError("Invalid saved approval fields.")

        return PendingApproval(
            gate=gate,
            binding=binding,
            asset_id=asset_id,
            operation=operation,
            proposal=proposal,
        )

    def _view(
        self,
        run_id: str,
        runtime: Runtime,
        snapshot: StateSnapshot,
    ) -> RunView:
        if not snapshot.values:
            raise RunNotFoundError(f"Run {run_id} was not found.")

        state = dict(snapshot.values)
        pending = self._pending(snapshot)

        if pending is not None:
            status = "awaiting_approval"
        elif snapshot.next:
            # Matches the CLI's restriction: do not silently resume an
            # execution that ended without reaching an approval checkpoint.
            status = "interrupted"
        else:
            status = str(state.get("status", "unknown"))

        return RunView(
            run_id=normalize_run_id(run_id),
            status=status,
            pending_approval=pending,
            state=state,
            stopped=runtime.stopped(),
        )

    def create_run(self) -> RunView:
        """Create a run and advance only to its first approval gate."""
        with _WORKFLOW_LOCK:
            run_id = str(uuid4())

            with self._session(run_id) as (runtime, graph, config):
                if runtime.stopped():
                    raise WorkflowConflictError(
                        "Emergency stop is active. Clear it locally before "
                        "starting a new investigation."
                    )

                graph.invoke({"status": "created"}, config)

                return self._view(
                    run_id,
                    runtime,
                    graph.get_state(config),
                )

    def get_run(self, run_id: str) -> RunView:
        """Read a checkpoint without invoking or resuming the graph."""
        with _WORKFLOW_LOCK:
            with self._session(run_id) as (runtime, graph, config):
                return self._view(
                    run_id,
                    runtime,
                    graph.get_state(config),
                )

    def decide(
        self,
        run_id: str,
        expected_gate: Gate,
        expected_binding: str,
        approved: bool,
    ) -> RunView:
        """Record a decision for the exact currently pending approval."""
        with _WORKFLOW_LOCK:
            with self._session(run_id) as (runtime, graph, config):
                snapshot = graph.get_state(config)
                current = self._view(run_id, runtime, snapshot)
                pending = current["pending_approval"]

                if pending is None:
                    raise WorkflowConflictError(
                        "This run has no pending approval. Refresh its state."
                    )

                if expected_gate != pending["gate"] or expected_binding != pending["binding"]:
                    raise WorkflowConflictError(
                        "The approval request changed. Refresh and review "
                        "the current request before deciding."
                    )

                if approved and runtime.stopped():
                    raise WorkflowConflictError(
                        "Emergency stop is active. Approval cannot proceed."
                    )

                # Trust the checkpoint's values, not browser-supplied bindings.
                runtime.record_approval(
                    pending["gate"],
                    pending["binding"],
                    approved,
                )

                try:
                    # This payload is deliberately not an authorization grant.
                    # The graph checks the operator-owned approval record.
                    graph.invoke(
                        Command(resume="operator_recorded"),
                        config,
                    )
                except PermissionError as exc:
                    # The current CLI graph does not convert PermissionError
                    # into a terminal failed state. Preserve its checkpoint
                    # and report the conflict instead of retrying execution.
                    runtime.audit(
                        "workflow_blocked",
                        {"message": str(exc)},
                    )
                    raise WorkflowConflictError(str(exc)) from exc

                return self._view(
                    run_id,
                    runtime,
                    graph.get_state(config),
                )

    def get_audit(self, run_id: str) -> list[AuditEvent]:
        """Return persisted audit events in database insertion order."""
        with _WORKFLOW_LOCK:
            with self._session(run_id) as (runtime, graph, config):
                # Verify that this UUID actually identifies a saved run.
                self._view(run_id, runtime, graph.get_state(config))

                rows = runtime.db.execute(
                    "SELECT id, at, action, details FROM audit WHERE run_id=? ORDER BY id",
                    (runtime.run_id,),
                ).fetchall()

                return [
                    AuditEvent(
                        id=row[0],
                        at=row[1],
                        action=row[2],
                        details=json.loads(row[3]),
                    )
                    for row in rows
                ]

    def activate_stop(self) -> dict[str, bool]:
        """Block subsequent tool attempts across runs using the existing flag.

        Deliberately does not acquire the workflow lock: an operator must
        be able to set STOP while a graph invocation is running.
        An already-started HTTP request is not forcibly interrupted.
        """
        self.directory.mkdir(parents=True, exist_ok=True)
        (self.directory / "STOP").touch(exist_ok=True)
        return {"stopped": True}
