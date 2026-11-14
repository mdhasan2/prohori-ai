from collections.abc import Iterator
from pathlib import Path
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from prohori_ai.application.local_workflow import Runtime
from prohori_ai.application.local_workflow_service import LocalWorkflowService
from prohori_ai.domain.security_asset import SecurityAsset
from prohori_ai.interfaces.api import create_app

ASSET_PAYLOAD: dict[str, object] = {
    "asset_id": "lab-api",
    "name": "Path-traversal lab API",
    "asset_type": "api",
    "record_origin": "synthetic",
    "verification_state": "unverified",
}


@pytest.fixture
def client(tmp_path: Path) -> Iterator[TestClient]:
    with TestClient(
        create_app(directory=tmp_path / "operator"),
        base_url="http://127.0.0.1",
        client=("127.0.0.1", 50000),
    ) as instance:
        yield instance


def test_inventory_contract_and_no_execution(
    client: TestClient,
    tmp_path: Path,
) -> None:
    with (
        patch.object(
            Runtime,
            "get_path",
            side_effect=AssertionError("Inventory must not contact a target."),
        ) as execute,
        patch.object(
            LocalWorkflowService,
            "create_run",
            side_effect=AssertionError("Inventory must not create a run."),
        ) as create_app,
    ):
        response = client.get("/api/assets")

        assert response.status_code == 200
        assert response.json() == [ASSET_PAYLOAD]

        execute.assert_not_called()
        create_app.assert_not_called()

    assert not (tmp_path / "operator").exists()


@pytest.mark.parametrize(
    "overrides",
    [
        {"asset_id": ""},
        {"asset_type": "unsupported"},
        {"verification_state": "verified"},
        {"human_approval_granted": True},
    ],
)
def test_invalid_asset_contract_is_rejected(
    overrides: dict[str, object],
) -> None:
    with pytest.raises(ValidationError):
        SecurityAsset.model_validate({**ASSET_PAYLOAD, **overrides})


def test_asset_is_frozen() -> None:
    asset = SecurityAsset.model_validate(ASSET_PAYLOAD)

    with pytest.raises(ValidationError):
        asset.name = "Changed"


def test_inventory_rejects_disallowed_origin(client: TestClient) -> None:
    response = client.get(
        "/api/assets",
        headers={"Origin": "https://untrusted.example"},
    )

    assert response.status_code == 403


def test_inventory_rejects_remote_peer(tmp_path: Path) -> None:
    with TestClient(
        create_app(directory=tmp_path / "operator"),
        base_url="http://127.0.0.1",
        client=("198.51.100.10", 50000),
    ) as remote:
        response = remote.get("/api/assets")

    assert response.status_code == 403


def test_inventory_has_no_write_endpoint(client: TestClient) -> None:
    response = client.post("/api/assets", json=ASSET_PAYLOAD)

    assert response.status_code == 405


def test_inventory_is_documented_in_openapi(client: TestClient) -> None:
    schema = client.get("/openapi.json").json()

    operation = schema["paths"]["/api/assets"]["get"]
    assert operation["operationId"] == "listSecurityAssets"

    properties = schema["components"]["schemas"]["SecurityAsset"]["properties"]
    assert properties["verification_state"]["const"] == "unverified"
