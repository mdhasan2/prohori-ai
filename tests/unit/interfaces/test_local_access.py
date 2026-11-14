from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from prohori_ai.application.local_workflow import Runtime
from prohori_ai.interfaces.api import create_app


@pytest.fixture
def local_app(tmp_path: Path) -> FastAPI:
    return create_app(directory=tmp_path / "operator")


@pytest.fixture
def client(local_app: FastAPI) -> Iterator[TestClient]:
    with TestClient(
        local_app,
        base_url="http://127.0.0.1",
        client=("127.0.0.1", 50000),
    ) as instance:
        yield instance


def test_health_exposes_local_access_contract(client: TestClient) -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "access_mode": "local_only",
    }

    schema = client.get("/openapi.json").json()
    properties = schema["components"]["schemas"]["HealthResponse"]["properties"]
    assert properties["access_mode"]["const"] == "local_only"


@pytest.mark.parametrize(
    "origin",
    ["http://127.0.0.1:5173", "http://localhost:5173"],
)
def test_allowed_ui_origin(client: TestClient, origin: str) -> None:
    response = client.get("/api/health", headers={"Origin": origin})

    assert response.status_code == 200


@pytest.mark.parametrize("origin", ["https://untrusted.example", "null"])
def test_disallowed_origin_blocks_reads_and_mutations(
    client: TestClient,
    tmp_path: Path,
    origin: str,
) -> None:
    read = client.get("/api/health", headers={"Origin": origin})
    mutation = client.post("/api/runs", json={}, headers={"Origin": origin})

    assert read.status_code == 403
    assert mutation.status_code == 403
    assert not (tmp_path / "operator").exists()


def test_invalid_host_is_rejected(client: TestClient) -> None:
    response = client.get(
        "/api/health",
        headers={"Host": "untrusted.example"},
    )

    assert response.status_code == 400


def test_remote_peer_cannot_spoof_local_access(
    local_app: FastAPI,
    tmp_path: Path,
) -> None:
    with TestClient(
        local_app,
        base_url="http://127.0.0.1",
        client=("198.51.100.10", 50000),
    ) as remote:
        for method, path in (
            ("GET", "/api/health"),
            ("POST", "/api/runs"),
            ("POST", "/api/stop"),
        ):
            response = remote.request(
                method,
                path,
                headers={"X-Forwarded-For": "127.0.0.1"},
            )

            assert response.status_code == 403
            assert response.json() == {
                "detail": "Local operator access only.",
            }

    assert not (tmp_path / "operator").exists()


def test_mutations_still_require_json(client: TestClient) -> None:
    response = client.post(
        "/api/runs",
        content="{}",
        headers={"Content-Type": "text/plain"},
    )

    assert response.status_code == 415


def test_local_create_reject_and_audit_preserve_approval_boundary(
    client: TestClient,
) -> None:
    with patch.object(
        Runtime,
        "get_path",
        side_effect=AssertionError("No target request should occur."),
    ) as execute:
        created = client.post("/api/runs", json={})

        assert created.status_code == 201
        run = created.json()
        assert run["status"] == "awaiting_approval"
        pending = run["pending_approval"]
        assert pending["gate"] == "investigation"

        rejected = client.post(
            f"/api/runs/{run['run_id']}/decision",
            json={
                "expected_gate": pending["gate"],
                "expected_binding": pending["binding"],
                "approved": False,
            },
        )

        assert rejected.status_code == 200
        assert rejected.json()["status"] == "cancelled"

        audit = client.get(f"/api/runs/{run['run_id']}/audit")
        assert audit.status_code == 200
        assert any(event["action"] == "operator_approval" for event in audit.json())

        execute.assert_not_called()
