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
    "owner_team": None,
    "environment": "lab",
    "data_classification": "unknown",
    "discovery_source": "demo_fixture",
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
        {"asset_id": "-lab-api"},
        {"owner_team": ""},
        {"owner_team": "  "},
        {"owner_team": "x" * 121},
        {"owner_team": 42},
        {"environment": "internet"},
        {"environment": None},
        {"data_classification": ""},
        {"data_classification": "secret"},
        {"data_classification": None},
        {"data_classification": 42},
        {"discovery_source": ""},
        {"discovery_source": "network_scan"},
        {"discovery_source": None},
        {"discovery_source": 42},
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

    assert properties["data_classification"]["default"] == "unknown"
    assert schema["components"]["schemas"]["DataClassification"]["enum"] == [
        "unknown",
        "public",
        "internal",
        "confidential",
        "restricted",
    ]

    assert properties["discovery_source"]["default"] == "unknown"
    assert schema["components"]["schemas"]["DiscoverySource"]["enum"] == [
        "unknown",
        "demo_fixture",
    ]


def test_missing_metadata_stays_unknown() -> None:
    asset = SecurityAsset.model_validate(
        {"asset_id": "unclassified-api", "name": "Unclassified demo API", "asset_type": "api"}
    )

    assert asset.owner_team is None
    assert asset.environment.value == "unknown"

    serialized = asset.model_dump(mode="json")
    assert serialized["owner_team"] is None
    assert serialized["environment"] == "unknown"
    assert asset.data_classification.value == "unknown"
    assert serialized["data_classification"] == "unknown"
    assert asset.discovery_source.value == "unknown"
    assert serialized["discovery_source"] == "unknown"


def test_known_metadata_does_not_change_verification() -> None:
    asset = SecurityAsset.model_validate(
        {
            **ASSET_PAYLOAD,
            "owner_team": "  Demo Platform Team  ",
            "environment": "production",
        }
    )

    assert asset.owner_team == "Demo Platform Team"
    assert asset.environment.value == "production"
    assert asset.record_origin == "synthetic"
    assert asset.verification_state == "unverified"


@pytest.mark.parametrize(
    "classification",
    ["unknown", "public", "internal", "confidential", "restricted"],
)
def test_classificaiton_does_not_grant_verification(classification: str) -> None:
    asset = SecurityAsset.model_validate(
        {
            **ASSET_PAYLOAD,
            "data_classification": classification,
        }
    )

    assert asset.model_dump(mode="json")["data_classification"] == classification
    assert asset.record_origin == "synthetic"
    assert asset.verification_state == "unverified"


@pytest.mark.parametrize("source", ["unknown", "demo_fixture"])
def test_discovery_source_does_not_grant_verification(source: str) -> None:
    asset = SecurityAsset.model_validate(
        {
            **ASSET_PAYLOAD,
            "discovery_source": source,
        }
    )

    assert asset.model_dump(mode="json")["discovery_source"] == source
    assert asset.record_origin == "synthetic"
    assert asset.verification_state == "unverified"
