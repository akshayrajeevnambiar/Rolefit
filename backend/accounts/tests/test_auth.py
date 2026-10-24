"""Session auth: register, login, logout, and the current user.

CSRF stays on. The tests use a client that rejects a missing token, which
is what a browser will see.
"""

import json

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.test import Client, override_settings

PASSWORD = "a-long-test-password-1"
OTHER_PASSWORD = "another-long-test-password-2"
MISMATCH = "That email and password don’t match."

pytestmark = pytest.mark.django_db


def csrf_client() -> tuple[Client, str]:
    client = Client(enforce_csrf_checks=True)
    response = client.get("/api/auth/csrf/")
    assert response.status_code == 204, response.content
    token = client.cookies["csrftoken"].value
    assert token
    return client, token


def post_json(client: Client, url: str, payload: dict[str, object], token: str):
    return client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_X_CSRFTOKEN=token,
    )


def current_token(client: Client) -> str:
    """The cookie after the last response.

    login() and logout() replace the CSRF cookie. The next call has to
    send that new value, which is what the browser will have stored.
    """
    return client.cookies["csrftoken"].value


def test_csrf_middleware_is_enabled() -> None:
    assert "django.middleware.csrf.CsrfViewMiddleware" in settings.MIDDLEWARE


def test_register_login_logout_and_me() -> None:
    client, token = csrf_client()

    created = post_json(
        client,
        "/api/auth/register/",
        {"email": "Ada@Example.com", "password": PASSWORD},
        token,
    )
    assert created.status_code == 201, created.content
    assert created.json() == {"id": created.json()["id"], "email": "ada@example.com"}
    assert PASSWORD not in created.content.decode()
    token = current_token(client)

    me = client.get("/api/auth/me/", HTTP_X_CSRFTOKEN=token)
    assert me.status_code == 200
    assert me.json()["email"] == "ada@example.com"

    logged_out = post_json(client, "/api/auth/logout/", {}, token)
    assert logged_out.status_code == 204
    token = current_token(client)
    assert client.get("/api/auth/me/", HTTP_X_CSRFTOKEN=token).status_code == 403

    logged_in = post_json(
        client,
        "/api/auth/login/",
        {"email": "ADA@example.com", "password": PASSWORD},
        token,
    )
    assert logged_in.status_code == 200, logged_in.content
    assert logged_in.json()["email"] == "ada@example.com"
    token = current_token(client)
    assert client.get("/api/auth/me/", HTTP_X_CSRFTOKEN=token).json()["email"] == (
        "ada@example.com"
    )


def test_register_and_login_reject_a_missing_csrf_token() -> None:
    client, _token = csrf_client()
    user_model = get_user_model()
    body = json.dumps({"email": "ada@example.com", "password": PASSWORD})

    rejected = client.post(
        "/api/auth/register/",
        data=body,
        content_type="application/json",
    )
    assert rejected.status_code == 403
    assert "CSRF" in rejected.json()["detail"]
    assert user_model.objects.count() == 0

    post_json(
        client,
        "/api/auth/register/",
        {"email": "ada@example.com", "password": PASSWORD},
        client.cookies["csrftoken"].value,
    )
    logged_out = Client(enforce_csrf_checks=True)
    logged_out.get("/api/auth/csrf/")
    denied = logged_out.post(
        "/api/auth/login/",
        data=json.dumps({"email": "ada@example.com", "password": PASSWORD}),
        content_type="application/json",
    )
    assert denied.status_code == 403
    assert "CSRF" in denied.json()["detail"]


def test_logout_rejects_a_missing_csrf_token() -> None:
    client, token = csrf_client()
    post_json(
        client,
        "/api/auth/register/",
        {"email": "ada@example.com", "password": PASSWORD},
        token,
    )
    token = current_token(client)

    denied = client.post(
        "/api/auth/logout/", data="{}", content_type="application/json"
    )
    assert denied.status_code == 403
    assert "CSRF" in denied.json()["detail"]
    assert client.get("/api/auth/me/", HTTP_X_CSRFTOKEN=token).status_code == 200


def test_wrong_password_does_not_start_a_session() -> None:
    client, token = csrf_client()
    post_json(
        client,
        "/api/auth/register/",
        {"email": "ada@example.com", "password": PASSWORD},
        token,
    )
    token = current_token(client)
    post_json(client, "/api/auth/logout/", {}, token)
    token = current_token(client)

    for email in ("ada@example.com", "nobody@example.com"):
        rejected = post_json(
            client,
            "/api/auth/login/",
            {"email": email, "password": OTHER_PASSWORD},
            token,
        )
        assert rejected.status_code == 400
        assert rejected.json() == {"detail": MISMATCH}
        assert client.get("/api/auth/me/", HTTP_X_CSRFTOKEN=token).status_code == 403


def test_duplicate_email_is_rejected() -> None:
    client, token = csrf_client()
    payload = {"email": "ada@example.com", "password": PASSWORD}
    assert post_json(client, "/api/auth/register/", payload, token).status_code == 201
    again = post_json(client, "/api/auth/register/", payload, current_token(client))
    assert again.status_code == 400
    assert get_user_model().objects.filter(email="ada@example.com").count() == 1


def test_very_long_password_is_rejected() -> None:
    """A megabyte password is a cheap way to burn CPU in the hasher."""
    client, token = csrf_client()
    rejected = post_json(
        client,
        "/api/auth/register/",
        {"email": "ada@example.com", "password": "x" * 129},
        token,
    )
    assert rejected.status_code == 400
    assert "password" in rejected.json()
    assert get_user_model().objects.count() == 0


def test_short_password_is_rejected() -> None:
    client, token = csrf_client()
    rejected = post_json(
        client,
        "/api/auth/register/",
        {"email": "ada@example.com", "password": "short"},
        token,
    )
    assert rejected.status_code == 400
    assert "password" in rejected.json()
    assert get_user_model().objects.count() == 0


def test_register_ignores_is_staff() -> None:
    client, token = csrf_client()
    created = post_json(
        client,
        "/api/auth/register/",
        {"email": "ada@example.com", "password": PASSWORD, "is_staff": True},
        token,
    )
    assert created.status_code == 201
    user = get_user_model().objects.get(email="ada@example.com")
    assert user.is_staff is False
    assert user.is_superuser is False
    assert user.check_password(PASSWORD)


def test_anonymous_me_is_rejected() -> None:
    client, token = csrf_client()
    assert client.get("/api/auth/me/", HTTP_X_CSRFTOKEN=token).status_code == 403


def test_auth_rate_limit_uses_the_connection_address() -> None:
    updated = {
        **settings.REST_FRAMEWORK,
        "DEFAULT_THROTTLE_RATES": {"auth": "2/min"},
    }
    with override_settings(REST_FRAMEWORK=updated):
        cache.clear()
        client, token = csrf_client()
        body = json.dumps({"email": "ada@example.com", "password": OTHER_PASSWORD})
        statuses = []
        for forwarded in ("203.0.113.1", "203.0.113.2", "203.0.113.3"):
            response = client.post(
                "/api/auth/login/",
                data=body,
                content_type="application/json",
                HTTP_X_CSRFTOKEN=token,
                HTTP_X_FORWARDED_FOR=forwarded,
                REMOTE_ADDR="198.51.100.10",
            )
            statuses.append(response.status_code)
        assert statuses == [400, 400, 429]
