from django.conf import settings
from django.http import HttpRequest
from django.test import RequestFactory
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def _closed(_request: HttpRequest) -> Response:
    return Response({"ok": True})


def test_new_routes_reject_anonymous_clients() -> None:
    response = _closed(RequestFactory().get("/closed/"))

    assert response.status_code == 403


def test_basic_authentication_is_not_enabled() -> None:
    assert settings.REST_FRAMEWORK["DEFAULT_PERMISSION_CLASSES"] == [
        "rest_framework.permissions.IsAuthenticated",
    ]
    assert settings.REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] == [
        "rest_framework.authentication.SessionAuthentication",
    ]
