import http.client
from collections.abc import Iterator
from pathlib import Path
from uuid import uuid4

import pytest
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.types import Command

from prohori_ai.agents.red.models import ValidationProposal
from prohori_ai.interfaces.cli import SCOPE_BINDING, Runtime, build_graph, proposal_binding


class Response:
    status = 200

    def getheaders(self) -> list[tuple[str, str]]:
        return [("content-type", "application/json")]


class Connection:
    calls = 0

    def __init__(self, host: str, port: int, *, timeout: int) -> None:
        assert (host, port, timeout) == ("127.0.0.1", 18080, 3)

    def request(self, method: str, path: str) -> None:
        assert (method, path) == ("GET", "/")
        Connection.calls += 1

    def getresponse(self) -> Response:
        return Response()

    def close(self) -> None:
        pass


@pytest.fixture
def runtime(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Runtime]:
    Connection.calls = 0
    monkeypatch.setattr(http.client, "HTTPConnection", Connection)
    isinstance = Runtime(tmp_path, str(uuid4()))
    yield isinstance
    isinstance.close()


def test_no_investigation_approval_means_no_request(runtime: Runtime) -> None:
    with pytest.raises(PermissionError):
        runtime.get_headers("http_get")
    assert Connection.calls == 0


def test_active_requires_bound_approval(runtime: Runtime) -> None:
    runtime.record_approval("investigation", SCOPE_BINDING, True)
    runtime.record_approval("validation", "different-purpose", True)
    with pytest.raises(PermissionError, match="approval_required"):
        runtime.get_headers("active_validation", "proposal-1")
    assert Connection.calls == 0


def test_complete_workflow_requires_both_approvals(runtime: Runtime, tmp_path: Path) -> None:
    config = {"configurable": {"thread_id": runtime.run_id}}
    with SqliteSaver.from_conn_string(str(tmp_path / "graph.sqlite")) as saver:
        graph = build_graph(runtime, saver)
        first = graph.invoke({"status": "created"}, config)
        assert first["__interrupt__"][0].value["gate"] == "investigation"
        assert Connection.calls == 0
        runtime.record_approval("investigation", SCOPE_BINDING, True)
        second = graph.invoke(Command(resume="operator_recorded"), config)
        assert second["__interrupt__"][0].value["gate"] == "validation"
        assert Connection.calls == 1
        proposal = ValidationProposal.model_validate(second["proposal"])
        runtime.record_approval("validation", proposal_binding(proposal), True)
        final = graph.invoke(Command(resume="operator_recorded"), config)
        assert final["status"] == "completed"
        assert len(final["evidence"]) == 2
        assert len(final["finding"]["evidence_ids"]) == 2
        assert Connection.calls == 2


def test_resume_payload_does_not_grant_approval(runtime: Runtime, tmp_path: Path) -> None:
    with SqliteSaver.from_conn_string(str(tmp_path / "graph.sqlite")) as saver:
        graph = build_graph(runtime, saver)
        config = {"configurable": {"thread_id": runtime.run_id}}
        graph.invoke({"status": "created"}, config)
        result = graph.invoke(Command(resume=True), config)
        assert result["status"] == "cancelled"
        assert Connection.calls == 0


def test_stop_and_expiry_block_requests(runtime: Runtime) -> None:
    runtime.record_approval("investigation", SCOPE_BINDING, True)
    (runtime.directory / "STOP").touch()
    with pytest.raises(PermissionError, match="Emergency stop"):
        runtime.get_headers("http_get")
    (runtime.directory / "STOP").unlink()
    runtime.db.execute("UPDATE approvals SET expires=0")
    runtime.db.commit()
    with pytest.raises(PermissionError, match="expired"):
        runtime.get_headers("http_get")
    assert Connection.calls == 0


def test_http_redirect_is_rejected(runtime: Runtime, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(Response, "status", 302)
    runtime.record_approval("investigation", SCOPE_BINDING, True)
    with pytest.raises(ValueError, match="no redirect followed"):
        runtime.get_headers("http_get")
    assert Connection.calls == 1
