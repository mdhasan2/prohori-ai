"""Single-operator local CLI slice. No LLM, arbitrary target, or shell execution."""

import argparse
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

from langchain_core.runnables import RunnableConfig
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.types import Command, interrupt

from prohori_ai.agents.red.models import (
    EvidenceKind,
    EvidenceRecord,
    HypothesisKind,
    SecurityHypothesis,
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
SCOPE_BINDING = "lab-api|http|127.0.0.1|18080|GET|/"
HEADER = "content-security-policy"
MAX_ATTEMPTS = 2
ACTION_LIMIT = 4


class State(TypedDict, total=False):
    status: str
    hypothesis: dict[str, Any]
    proposal: dict[str, Any]
    evidence: list[dict[str, Any]]
    finding: dict[str, Any]
    error: str


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

    def get_headers(self, capability: str, binding: str = "") -> dict[str, str]:
        """Only GET / on the fixed loopback lab; redirects are never followed."""
        deadline = monotonic() + 8
        for attempt in range(1, MAX_ATTEMPTS + 1):
            if self.stopped():
                raise PermissionError("Emergency stop is active")
            if not self.approved("investigation", SCOPE_BINDING):
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
                    target="127.0.0.1",
                    human_approval_granted=self.approved("validation", binding),
                ),
                scope=self.scope,
                budget=ActionBudget(limit=ACTION_LIMIT, consumed=consumed),
                emergency_stop=EmergencyStop(enabled=self.stopped()),
            )
            self.audit("policy_decision", decision.model_dump(mode="json"))
            if not decision.allowed:
                raise PermissionError(decision.code.value)
            if monotonic() >= deadline:
                raise TimeoutError("Tool deadline exceeded")
            # This committed record also consumes one budget unit, including failed attempts.
            self.audit("execution_intent", {"capability": capability, "attempt": attempt})
            connection = http.client.HTTPConnection("127.0.0.1", 18080, timeout=3)
            try:
                connection.request("GET", "/")
                response = connection.getresponse()
                if response.status != 200:
                    raise ValueError(
                        f"Excepted 200; received {response.status}; no redirect followed"
                    )
                headers = {name.lower(): value for name, value in response.getheaders()}
                self.audit("execution_result", {"capability": capability, "status": 200})
                return headers
            except (OSError, http.client.HTTPException) as exc:
                self.audit("execution_error", {"type": type(exc).__name__, "attempt": attempt})
                if attempt == MAX_ATTEMPTS:
                    raise
            finally:
                connection.close()
        raise RuntimeError("Unreachable retry state")


def build_graph(
    runtime: Runtime, saver: SqliteSaver
) -> CompiledStateGraph[State, None, State, State]:
    def gate(state: State, kind: str, binding: str) -> State:
        interrupt(
            {
                "gate": kind,
                "binding": binding,
                "asset_id": ASSET_ID,
                "operation": "GET http://127.0.0.1:18080/; inspect Content-Security-Policy header",
                "proposal": state.get("proposal"),
            }
        )
        # Resume payload is not authorization: consult the operator-owned record.
        allowed = runtime.approved(kind, binding) and not runtime.stopped()
        return {"status": "approved" if allowed else "cancelled"}

    def scope_gate(state: State) -> State:
        return gate(state, "investigation", SCOPE_BINDING)

    def red(state: State) -> State:
        headers = runtime.get_headers("http_get")
        print(headers)
        if HEADER in headers:
            return {"status": "completed", "evidence": []}
        hypothesis = SecurityHypothesis(
            hypothesis_id=str(uuid4()),
            asset_id=ASSET_ID,
            kind=HypothesisKind.MISSING_SECURITY_HEADER,
            rationale="GET / returned no CSP header; validate before confirmation.",
        )
        evidence = EvidenceRecord(
            evidence_id=str(uuid4()),
            asset_id=ASSET_ID,
            hypothesis_id=hypothesis.hypothesis_id,
            kind=EvidenceKind.PASSIVE_HTTP_METADATA,
            source="http://127.0.0.1:18080/",
            summary="Content-Security-Policy header absent in the initial response.",
            collected_at=datetime.now(UTC),
        )
        proposal = propose_validation(hypothesis, (evidence,))
        if proposal is None:
            raise ValueError("Evidence did not support a proposal")
        runtime.audit("proposal_created", proposal.model_dump(mode="json"))
        return {
            "status": "proposed",
            "hypothesis": hypothesis.model_dump(mode="json"),
            "evidence": [evidence.model_dump(mode="json")],
            "proposal": proposal.model_dump(mode="json"),
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
            or proposal.hypothesis_id != hypothesis.hypothesis_id
            or proposal.evidence_ids != tuple(item.evidence_id for item in evidence)
            or any(
                item.asset_id != ASSET_ID or item.hypothesis_id != hypothesis.hypothesis_id
                for item in evidence
            )
        ):
            raise ValueError("Proposal/evidence binding rejected")
        headers = runtime.get_headers("active_validation", proposal_binding(proposal))
        missing = HEADER not in headers
        active = EvidenceRecord(
            evidence_id=str(uuid4()),
            asset_id=ASSET_ID,
            hypothesis_id=hypothesis.hypothesis_id,
            kind=EvidenceKind.ACTIVE_VALIDATION,
            source="http://127.0.0.1:18080/",
            summary=f"Approved recheck: Content-Security-Policy absent={missing}",
            collected_at=datetime.now(UTC),
        )
        finding = Finding(
            investigation_id=UUID(runtime.run_id),
            title="Missing Content-Security-Policy header",
            description="Local lab root response lacks CSP, Assess impact seperately.",
            status=FindingStatus.CONFIRMED if missing else FindingStatus.REJECTED,
            evidence_ids=tuple(UUID(item.evidence_id) for item in [*evidence, active]),
        )
        runtime.audit("finding_created", finding.model_dump(mode="json"))
        return {
            "status": "completed",
            "finding": finding.model_dump(mode="json"),
            "evidence": [item.model_dump(mode="json") for item in [*evidence, active]],
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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resume", metavar="RUN_ID")
    args = parser.parse_args()
    run_id = str(UUID(args.resume)) if args.resume else str(uuid4())
    directory = Path(".prohori-cli")
    runtime = Runtime(directory, run_id)
    print(f"Run ID: {run_id}")
    print("Target: http://127.0.0.1:18080/ (fixed local lab)")
    try:
        with SqliteSaver.from_conn_string(str(directory / "checkpoints.sqlite")) as saver:
            graph = build_graph(runtime, saver)
            config: RunnableConfig = {"configurable": {"thread_id": run_id}}
            if args.resume:
                snapshot = graph.get_state(config)
                if not snapshot.values:
                    parser.error("Unknwon run ID")
                if snapshot.next and not snapshot.interrupts:
                    parser.error("Run was interrupted during execution; start a new run")
                result = dict(snapshot.values)
                result["__interrupt__"] = snapshot.interrupts
            else:
                result = graph.invoke({"status": "created"}, config)
            while result.get("__interrupt__"):
                request = result["__interrupt__"][0].value
                print(json.dumps(request, indent=2))
                print("Type approve to authorize; Enter to reject; pause to exit and resume later.")
                try:
                    answer = input("> ").strip().lower()
                except EOFError:
                    answer = "pause"
                if answer == "pause":
                    print(
                        "Paused. Resuem: uv run python -m prohori_ai.interfaces.cli "
                        f"--resume {run_id}"
                    )
                    return
                runtime.record_approval(request["gate"], request["binding"], answer == "approve")
                result = graph.invoke(Command(resume="operator_recorded"), config)
            final = graph.get_state(config).values
            print(json.dumps(final, indent=2))
            if final.get("status") == "failed":
                raise SystemExit(1)
    except KeyboardInterrupt:
        print("Interrupted. Pending approval checkpoints can be resumed with the Run ID.")
        raise SystemExit(130) from None
    finally:
        runtime.close()


if __name__ == "__main__":
    main()
