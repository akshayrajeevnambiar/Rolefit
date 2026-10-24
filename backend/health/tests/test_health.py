from django.test import Client
from rest_framework.permissions import AllowAny

from health.views import health


def test_health_is_public() -> None:
    """The liveness route opts out of the IsAuthenticated default."""
    assert health.cls.permission_classes == [AllowAny]

    response = Client().get("/api/health/")

    assert response.status_code == 200
    assert response["Content-Type"].startswith("application/json")
    assert response.json() == {"status": "ok"}
