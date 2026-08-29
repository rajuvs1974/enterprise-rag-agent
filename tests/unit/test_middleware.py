from fastapi.testclient import TestClient

from erap.main import app

client = TestClient(app)


def test_request_id_is_generated() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers.get("X-Request-ID")


def test_request_id_is_preserved() -> None:
    request_id = "portfolio-test-001"

    response = client.get(
        "/health",
        headers={"X-Request-ID": request_id},
    )

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == request_id
