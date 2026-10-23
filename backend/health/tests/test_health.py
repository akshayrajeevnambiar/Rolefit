from django.test import Client


def test_health_returns_ok() -> None:
    response = Client().get("/api/health/")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/json")
    assert response.json() == {"status": "ok"}
