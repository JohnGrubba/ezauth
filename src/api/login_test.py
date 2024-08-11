from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


# SUCCESSFUL TESTS
def test_login_email_identifier(fixtureuser):
    response = client.post(
        "/login",
        json={"identifier": fixtureuser["email"], "password": fixtureuser["password"]},
    )
    resp_js = response.json()
    assert response.status_code == 200
    assert resp_js.get("session_token") is not None
    assert int(resp_js.get("expires")) is not None


def test_login_username_identifier(fixtureuser):
    response = client.post(
        "/login",
        json={
            "identifier": fixtureuser["username"],
            "password": fixtureuser["password"],
        },
    )
    resp_js = response.json()
    assert response.status_code == 200
    assert resp_js.get("session_token") is not None
    assert int(resp_js.get("expires")) is not None


# INVALID PASSWORD
def test_login_invalid_password(fixtureuser):
    response = client.post(
        "/login",
        json={
            "identifier": fixtureuser["username"],
            "password": "DefinitelyWrongPassword",
        },
    )
    resp_js = response.json()
    assert resp_js["detail"] == "Invalid Password"
    assert response.status_code == 401


# TEST UNKNOWN USER
def test_login_unknown_username(fixtureuser):
    response = client.post(
        "/login",
        json={
            "identifier": "existiertnicht",
            "password": "DefinitelyWrongPassword",
        },
    )
    resp_js = response.json()
    assert resp_js["detail"] == "User not found"
    assert response.status_code == 404


# TEST MISSING CREDENTIALS
def test_login_missing_password():
    response = client.post(
        "/login",
        json={"identifier": "joaaa"},
    )
    resp_js = response.json()
    assert response.status_code == 422
    assert resp_js["detail"][0]["msg"] == "Field required"
    assert resp_js["detail"][0]["loc"] == ["body", "password"]


def test_login_missing_identifier():
    response = client.post(
        "/login",
        json={"password": "joaaaa"},
    )
    resp_js = response.json()
    assert response.status_code == 422
    assert resp_js["detail"][0]["msg"] == "Field required"
    assert resp_js["detail"][0]["loc"] == ["body", "identifier"]


def test_login_maximum_attempts(fixtureuser):
    for _ in range(5):
        response = client.post(
            "/login",
            json={
                "identifier": fixtureuser["email"],
                "password": "DefinitelyWrongPassword",
            },
        )
    assert response.status_code == 429
