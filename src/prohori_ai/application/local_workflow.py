import hashlib
import http.client
import json
import sqlite3
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from time import monotonic, time
from typing import Any, TypedDict
from uuid import UUID, uuid4

from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command, interrupt

from prohori_ai.agents.red.models import (
    EvidenceKind,
    EvidenceRecord,
    HypothesisKind,
    SecurityHypothesis,
    ValidationKind,
    ValidationProposal,
)
from prohori_ai.agents.red.proposals import propose_validation
from prohori_ai.domain.finding import Finding, FindingStatus
from prohori_ai.policy.capabilities import CapabilityRegistry
from prohori_ai.policy.engine import PolicyEngine
from prohori_ai.policy.models import (
    ActionBudget,
    AuthorizationRequest,
    CapabilityClass,
    EmergencyStop,
    ScopePolicy,
    TargetRule,
    TargetRuleKind,
    ToolCapability,
)

ASSET_ID = "lab-api"

HOST = "127.0.0.1"
PORT = 18080

PUBLIC_PATH = "/files/readme.txt"

TRAVERSAL_PATH = "/files/../private/proof.txt"

PROOF_MARKER = "PROHORI_PATH_TRAVERSAL_PROOF"

SCOPE_BINDING = f"{ASSET_ID}|http|{HOST}|{PORT}|GET|{PUBLIC_PATH}|validate:{TRAVERSAL_PATH}"

MAX_ATTEMPTS = 2
ACTION_LIMIT = 4


class State(TypedDict, total=False):
    status: str
    hypothesis: dict[str, Any]
    proposal: dict[str, Any]
    evidence: list[dict[str, Any]]
    finding: dict[str, Any]
    error: str


class HttpResult(TypedDict):
    status: int
    body: str


def proposal_binding(proposal: ValidationProposal) -> str:
    payload = json.dumps(proposal.model_dump(mode="json"), sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()


class Runtime:
    """Trusted operator runtime; never pass this object to a model."""

    def __init__(self, directory: Path, run_id: str) -> None:
        self.directory = directory
        self.run_id = str(UUID(run_id))
        directory.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(directory / "operator.sqlite")
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS approvals "
            "(run_id TEXT, gate TEXT, binding TEXT, approved INTEGER, expires REAL, "
            "PRIMARY KEY(run_id, gate))"
        )
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS audit "
            "(id INTEGER PRIMARY KEY, run_id TEXT, at TEXT, action TEXT, details TEXT)"
        )
        self.db.commit()
        self.engine = PolicyEngine(
            CapabilityRegistry(
                [
                    ToolCapability(name="http_get", capability_class=CapabilityClass.PASSIVE),
                    ToolCapability(
                        name="active_validation", capability_class=CapabilityClass.ACTIVE
                    ),
                ]
            )
        )
        self.scope = ScopePolicy(
            allowed_targets=(TargetRule(kind=TargetRuleKind.EXACT_HOST, value="127.0.0.1"),)
        )

    def close(self) -> None:
        self.db.close()

    def audit(self, action: str, details: dict[str, Any]) -> None:
        self.db.execute(
            "INSERT INTO audit(run_id, at, action, details) VALUES (?, ?, ?, ?)",
            (self.run_id, datetime.now(UTC).isoformat(), action, json.dumps(details)),
        )
        self.db.commit()

    def record_approval(self, gate: str, binding: str, approved: bool) -> None:
        self.db.execute(
            "INSERT OR REPLACE INTO approvals VALUES (?, ?, ?, ?, ?)",
            (self.run_id, gate, binding, int(approved), time() + 300),
        )
        self.db.commit()
        self.audit("operator_approval", {"gate": gate, "binding": binding, "approved": approved})

    def approved(self, gate: str, binding: str) -> bool:
        row = self.db.execute(
            "SELECT binding, approved, expires FROM approvals WHERE run_id=? AND gate=?",
            (self.run_id, gate),
        ).fetchone()
        return bool(row and row[0] == binding and row[1] == 1 and row[2] > time())

    def stopped(self) -> bool:
        return (self.directory / "STOP").exists()

    def get_path(
        self,
        capability: str,
        path: str,
        binding: str = "",
    ) -> HttpResult:
        """Perform one explicitly allowlisted local HTTP request."""

        allowed_paths = {
            "http_get": PUBLIC_PATH,
            "active_validation": TRAVERSAL_PATH,
        }

        expected_path = allowed_paths.get(
            capability,
        )

        if expected_path is None:
            raise PermissionError("Capability has no HTTP path mapping")

        if path != expected_path:
            raise PermissionError("Path is not allowlisted for capability")

        deadline = monotonic() + 8

        for attempt in range(
            1,
            MAX_ATTEMPTS + 1,
        ):
            if self.stopped():
                raise PermissionError("Emergency stop is active")

            if not self.approved(
                "investigation",
                SCOPE_BINDING,
            ):
                raise PermissionError("Investigation approval is missing or expired")

            consumed = int(
                self.db.execute(
                    "SELECT COUNT(*) FROM audit WHERE run_id=? AND action='execution_intent'",
                    (self.run_id,),
                ).fetchone()[0]
            )

            decision = self.engine.authorize(
                request=AuthorizationRequest(
                    tool_name=capability,
                    target=HOST,
                    human_approval_granted=(
                        self.approved(
                            "validation",
                            binding,
                        )
                    ),
                ),
                scope=self.scope,
                budget=ActionBudget(
                    limit=ACTION_LIMIT,
                    consumed=consumed,
                ),
                emergency_stop=EmergencyStop(
                    enabled=self.stopped(),
                ),
            )

            self.audit(
                "policy_decision",
                decision.model_dump(
                    mode="json",
                ),
            )

            if not decision.allowed:
                raise PermissionError(decision.code.value)

            if monotonic() >= deadline:
                raise TimeoutError("Tool deadline exceeded")

            self.audit(
                "execution_intent",
                {
                    "capability": capability,
                    "path": path,
                    "attempt": attempt,
                },
            )

            connection = http.client.HTTPConnection(
                HOST,
                PORT,
                timeout=3,
            )

            try:
                connection.request(
                    "GET",
                    path,
                )

                response = connection.getresponse()

                body = response.read().decode(
                    "utf-8",
                    errors="replace",
                )

                allowed_statuses = {200} if capability == "http_get" else {200, 403, 404}

                if response.status not in allowed_statuses:
                    raise ValueError(
                        f"Unexpected HTTP status {response.status}: no redirect followed"
                    )

                self.audit(
                    "execution_result",
                    {
                        "capability": capability,
                        "path": path,
                        "status": response.status,
                    },
                )

                return {
                    "status": response.status,
                    "body": body,
                }

            except (
                OSError,
                http.client.HTTPException,
            ) as exc:
                self.audit(
                    "execution_error",
                    {
                        "type": type(exc).__name__,
                        "attempt": attempt,
                    },
                )

                if attempt == MAX_ATTEMPTS:
                    raise

            finally:
                connection.close()

        raise RuntimeError("Unreachable retry state")


def build_graph(
    runtime: Runtime, saver: SqliteSaver
) -> CompiledStateGraph[State, None, State, State]:
    def gate(state: State, kind: str, binding: str) -> State:

        if kind == "investigation":
            operation = (
                f"GET http://{HOST}:{PORT}"
                f"{PUBLIC_PATH}; "
                "passively inspect the public lab file endpoint"
            )
        else:
            operation = (
                f"GET http://{HOST}:{PORT}"
                f"{TRAVERSAL_PATH}; "
                "attempt one controlled path-traversal read "
                "inside the diposable lab"
            )

        interrupt(
            {
                "gate": kind,
                "binding": binding,
                "asset_id": ASSET_ID,
                "operation": operation,
                "proposal": state.get("proposal"),
            }
        )

        # Resume payload is not authorization: consult the operator-owned record.
        allowed = runtime.approved(kind, binding) and not runtime.stopped()
        return {"status": "approved" if allowed else "cancelled"}

    def scope_gate(state: State) -> State:
        return gate(state, "investigation", SCOPE_BINDING)

    def red(state: State) -> State:
        del state

        response = runtime.get_path(
            "http_get",
            PUBLIC_PATH,
        )

        if response["status"] != 200:
            raise ValueError("Public lab file was not readable")

        hypothesis = SecurityHypothesis(
            hypothesis_id=str(uuid4()),
            asset_id=ASSET_ID,
            kind=HypothesisKind.PATH_TRAVERSAL,
            rationale=(
                "The authorized file endpoint accepts a path "
                "component and returned the expected public file. "
                "A controlled active validation is required to "
                "determine whether the public-directory boundary "
                "can be escaped."
            ),
        )

        evidence = EvidenceRecord(
            evidence_id=str(uuid4()),
            asset_id=ASSET_ID,
            hypothesis_id=hypothesis.hypothesis_id,
            kind=(EvidenceKind.PASSIVE_HTTP_METADATA),
            source=(f"http://{HOST}:{PORT}{PUBLIC_PATH}"),
            summary=(
                "Authorized public file read succeeded. "
                "No traversal was attempted during passive "
                "evidence collection."
            ),
            collected_at=datetime.now(UTC),
        )

        proposal = propose_validation(
            hypothesis,
            (evidence,),
        )

        if proposal is None:
            raise ValueError("Evidence did not support a proposal")

        runtime.audit(
            "proposal_created",
            proposal.model_dump(
                mode="json",
            ),
        )

        return {
            "status": "proposed",
            "hypothesis": (
                hypothesis.model_dump(
                    mode="json",
                )
            ),
            "evidence": [
                evidence.model_dump(
                    mode="json",
                )
            ],
            "proposal": (
                proposal.model_dump(
                    mode="json",
                )
            ),
        }

    def validation_gate(state: State) -> State:
        proposal = ValidationProposal.model_validate(state["proposal"])
        return gate(state, "validation", proposal_binding(proposal))

    def validate(state: State) -> State:
        proposal = ValidationProposal.model_validate(state["proposal"])

        hypothesis = SecurityHypothesis.model_validate(state["hypothesis"])

        evidence = [EvidenceRecord.model_validate(item) for item in state["evidence"]]

        if (
            proposal.asset_id != ASSET_ID
            or hypothesis.asset_id != ASSET_ID
            or proposal.requested_capability != "active_validation"
            or proposal.validation_kind is not ValidationKind.CHECK_PATH_TRAVERSAL
            or proposal.hypothesis_id != hypothesis.hypothesis_id
            or proposal.evidence_ids != tuple(item.evidence_id for item in evidence)
            or any(
                (item.asset_id != ASSET_ID or item.hypothesis_id != hypothesis.hypothesis_id)
                for item in evidence
            )
        ):
            raise ValueError("Proposal/evidence binding rejected")

        response = runtime.get_path(
            "active_validation",
            TRAVERSAL_PATH,
            proposal_binding(proposal),
        )

        traversal_succeeded = response["status"] == 200 and PROOF_MARKER in response["body"]

        active = EvidenceRecord(
            evidence_id=str(uuid4()),
            asset_id=ASSET_ID,
            hypothesis_id=hypothesis.hypothesis_id,
            kind=EvidenceKind.ACTIVE_VALIDATION,
            source=(f"http://{HOST}:{PORT}{TRAVERSAL_PATH}"),
            summary=(
                "Approved path-traversal validation:"
                f"status={response['status']}; "
                "private proof observed="
                f"{traversal_succeeded}"
            ),
            collected_at=datetime.now(UTC),
        )

        finding = Finding(
            investigation_id=UUID(runtime.run_id),
            title=(
                "Path traversal allows read outside "
                "read the private proof outside the intended "
                "public directory."
            ),
            description=(
                "The approved local traversal validation "
                "read the private proof outside the intended "
                "public directory."
                if traversal_succeeded
                else (
                    "The approved traversal request did not "
                    "return the private proof. The diectory "
                    "boundary prevented reproduction."
                )
            ),
            status=(FindingStatus.CONFIRMED if traversal_succeeded else FindingStatus.REJECTED),
            evidence_ids=tuple(
                UUID(item.evidence_id)
                for item in [
                    *evidence,
                    active,
                ]
            ),
        )

        runtime.audit(
            "finding_created",
            finding.model_dump(
                mode="json",
            ),
        )

        return {
            "status": "completed",
            "finding": finding.model_dump(
                mode="json",
            ),
            "evidence": [
                item.model_dump(
                    mode="json",
                )
                for item in [
                    *evidence,
                    active,
                ]
            ],
        }

    def guarded(node: Callable[[State], State], state: State) -> State:
        try:
            return node(state)
        except (OSError, http.client.HTTPException, ValueError) as exc:
            runtime.audit("workflow_failed", {"type": type(exc).__name__, "message": str(exc)})
            return {"status": "failed", "error": str(exc)}

    def red_node(state: State) -> State:
        return guarded(red, state)

    def validate_node(state: State) -> State:
        return guarded(validate, state)

    graph = StateGraph[State, None, State, State](State)
    graph.add_node("scope_gate", scope_gate)
    graph.add_node("red", red_node)
    graph.add_node("validation_gate", validation_gate)
    graph.add_node("validate", validate_node)
    graph.add_edge(START, "scope_gate")
    graph.add_conditional_edges("scope_gate", lambda s: "red" if s["status"] == "approved" else END)
    graph.add_conditional_edges(
        "red", lambda s: "validation_gate" if s["status"] == "proposed" else END
    )
    graph.add_conditional_edges(
        "validation_gate", lambda s: "validate" if s["status"] == "approved" else END
    )
    graph.add_edge("validate", END)
    return graph.compile(checkpointer=saver)
