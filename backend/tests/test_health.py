from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_live_returns_ok():
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_valid_request_id_is_echoed():
    response = client.get("/api/v1/health/live", headers={"X-Request-ID": "abc-123"})
    assert response.headers["X-Request-ID"] == "abc-123"


def test_invalid_request_id_is_replaced():
    bad = "has spaces and ! symbols"
    response = client.get("/api/v1/health/live", headers={"X-Request-ID": bad})
    assert response.headers["X-Request-ID"] != bad
