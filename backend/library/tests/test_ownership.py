"""A person can read and change only their own résumés and descriptions."""

import json

import pytest
from django.test import Client

PASSWORD = "a-long-test-password-1"
PASTE_LIMIT = 100_000

pytestmark = pytest.mark.django_db


def sign_in(email: str) -> tuple[Client, str]:
    client = Client(enforce_csrf_checks=True)
    assert client.get("/api/auth/csrf/").status_code == 204
    token = client.cookies["csrftoken"].value
    created = client.post(
        "/api/auth/register/",
        data=json.dumps({"email": email, "password": PASSWORD}),
        content_type="application/json",
        HTTP_X_CSRFTOKEN=token,
    )
    assert created.status_code == 201, created.content
    return client, client.cookies["csrftoken"].value


def post_json(client: Client, url: str, payload: dict[str, object], token: str):
    return client.post(
        url,
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_X_CSRFTOKEN=token,
    )


def patch_json(client: Client, url: str, payload: dict[str, object], token: str):
    return client.patch(
        url,
        data=json.dumps(payload),
        content_type="application/json",
        HTTP_X_CSRFTOKEN=token,
    )


def delete(client: Client, url: str, token: str):
    return client.delete(url, HTTP_X_CSRFTOKEN=token)


CASES = [
    (
        "/api/resumes/",
        {"title": "Main", "text": "ALICE-PRIVATE-RESUME"},
    ),
    (
        "/api/job-descriptions/",
        {
            "company": "Northwind Health",
            "role": "Backend engineer",
            "text": "ALICE-PRIVATE-DESCRIPTION",
        },
    ),
]


@pytest.mark.parametrize(("collection", "payload"), CASES)
def test_another_account_cannot_read_or_change_a_record(
    collection: str,
    payload: dict[str, str],
) -> None:
    alice, alice_token = sign_in("alice@example.com")
    bob, bob_token = sign_in("bob@example.com")
    private = payload["text"]

    created = post_json(alice, collection, payload, alice_token)
    assert created.status_code == 201, created.content
    body = created.json()
    assert body["text"] == private
    assert "owner" not in body
    url = f"{collection}{body['id']}/"

    bob_list = bob.get(f"{collection}?owner={body['id']}", HTTP_X_CSRFTOKEN=bob_token)
    assert bob_list.status_code == 200
    assert bob_list.json() == []
    assert private not in bob_list.content.decode()

    for response in (
        bob.get(url, HTTP_X_CSRFTOKEN=bob_token),
        patch_json(bob, url, {"text": "taken"}, bob_token),
        delete(bob, url, bob_token),
    ):
        assert response.status_code == 404
        assert private not in response.content.decode()
        assert "taken" not in response.content.decode()

    still = alice.get(url, HTTP_X_CSRFTOKEN=alice_token)
    assert still.status_code == 200
    assert still.json()["text"] == private


@pytest.mark.parametrize(("collection", "payload"), CASES)
def test_create_stores_the_caller_even_if_the_body_names_someone_else(
    collection: str,
    payload: dict[str, str],
) -> None:
    alice, alice_token = sign_in("alice@example.com")
    _bob, _bob_token = sign_in("bob@example.com")
    created = post_json(
        alice,
        collection,
        {**payload, "owner": 999},
        alice_token,
    )
    assert created.status_code == 201, created.content
    url = f"{collection}{created.json()['id']}/"

    listed = alice.get(collection, HTTP_X_CSRFTOKEN=alice_token)
    assert listed.status_code == 200
    assert [row["id"] for row in listed.json()] == [created.json()["id"]]

    revised = patch_json(
        alice,
        url,
        {"text": payload["text"] + " revised", "owner": 999},
        alice_token,
    )
    assert revised.status_code == 200
    assert revised.json()["text"].endswith(" revised")
    assert "owner" not in revised.json()

    removed = delete(alice, url, alice_token)
    assert removed.status_code == 204
    assert alice.get(url, HTTP_X_CSRFTOKEN=alice_token).status_code == 404


def test_anonymous_cannot_list_records() -> None:
    client = Client()
    assert client.get("/api/resumes/").status_code == 403
    assert client.get("/api/job-descriptions/").status_code == 403


def test_blank_or_huge_paste_is_rejected() -> None:
    alice, token = sign_in("alice@example.com")
    for text in ("", "   ", "x" * (PASTE_LIMIT + 1)):
        rejected = post_json(alice, "/api/resumes/", {"text": text}, token)
        assert rejected.status_code == 400, rejected.content
    assert alice.get("/api/resumes/", HTTP_X_CSRFTOKEN=token).json() == []

    missing = post_json(
        alice,
        "/api/job-descriptions/",
        {"company": "  ", "role": "Backend engineer", "text": "Python"},
        token,
    )
    assert missing.status_code == 400
    assert alice.get("/api/job-descriptions/", HTTP_X_CSRFTOKEN=token).json() == []


def test_there_is_no_analysis_route() -> None:
    alice, token = sign_in("alice@example.com")
    assert alice.get("/api/analyses/", HTTP_X_CSRFTOKEN=token).status_code == 404
