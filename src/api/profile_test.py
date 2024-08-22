from fastapi.testclient import TestClient
from crud.user import get_dangerous_user

from .main import app

client = TestClient(app)


# Unauthorized Route Test
def test_unauthorized_profile():
    response = client.get("/profile")
    assert response.status_code == 401


def test_get_profile_invalid_session():
    client.cookies.set("session", "invalid")
    response = client.get("/profile")
    assert response.status_code == 401


# Successfull tests
def test_get_profile(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.get("/profile")
    resp_json = response.json()
    assert response.status_code == 200
    assert resp_json.get("email") == fixturesessiontoken_user[1]["email"]
    assert resp_json.get("username") == fixturesessiontoken_user[1]["username"]
    assert resp_json.get("createdAt") is not None
    assert resp_json.get("password") is None
    assert resp_json.get("_id") is not None


def test_update_username_valid(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.patch("/profile", json={"username": "newusername"})
    resp_json = response.json()
    assert response.status_code == 200
    assert resp_json.get("email") == fixturesessiontoken_user[1]["email"]
    assert resp_json.get("username") == "newusername"
    assert resp_json.get("createdAt") is not None


def test_update_password(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    # Password should not be updateable through this endpoint
    response = client.patch("/profile", json={"password": "Kennwort2!"})
    assert response.status_code == 200
    assert (
        get_dangerous_user(fixturesessiontoken_user[1]["_id"])["password"]
        != "Kennwort2!"
    )


def test_update_createdAt(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    # Password should not be updateable through this endpoint
    response = client.patch("/profile", json={"createdAt": "1921"})
    assert response.status_code == 200
    assert get_dangerous_user(fixturesessiontoken_user[1]["_id"])["createdAt"] != "1921"


def test_update_additional_data_valid(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    # Data that is not existent, but updateable should be possible
    response = client.patch("/profile", json={"test2": "1921"})
    assert response.status_code == 200
    assert get_dangerous_user(fixturesessiontoken_user[1]["_id"]).get("test2") == "1921"


def test_update_nonexistent_data(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    # Additional data should not be updateable through this endpoint
    response = client.patch("/profile", json={"sas": "1921"})
    assert response.status_code == 200
    assert get_dangerous_user(fixturesessiontoken_user[1]["_id"]).get("sas") is None


def test_update_additional_existent_data(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    # Data that is additional but already exists should also be updateable
    response = client.patch("/profile", json={"test": "Ya"})
    assert response.status_code == 200
    assert get_dangerous_user(fixturesessiontoken_user[1]["_id"]).get("test") == "Ya"


def test_update_username_taken(fixturesessiontoken_user, fixturesessiontoken_user2):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.patch(
        "/profile", json={"username": fixturesessiontoken_user2[1]["username"]}
    )
    assert response.status_code == 409
    assert response.json().get("detail") == "Username already in use."
