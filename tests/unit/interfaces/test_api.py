from fastapi.testclient import TestClient

from prohori_ai.interfaces.api import app


def test_health_endpoint() -> None:
    client = TestClient(
        app,
        base_url="http://127.0.0.1",
        client=("127.0.0.1", 50000),
    )

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
    }
