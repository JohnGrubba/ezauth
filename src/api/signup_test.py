from fastapi.testclient import TestClient
from tools import users_collection

from .main import app

client = TestClient(app)


# SUCCESSFUL TESTS
def test_create_account():
    response = client.post(
        "/signup",
        json={
            "password": "Kennwort1!",
            "email": "user@example.com",
            "username": "string",
        },
    )
    resp_js = response.json()
    assert response.status_code == 200
    assert resp_js.get("session_token") is not None
    assert int(resp_js.get("expires")) is not None


def test_create_account_additional_data():
    response = client.post(
        "/signup",
        json={
            "password": "Kennwort1!",
            "email": "user1@example.com",
            "username": "string1",
            "test": True,
            "test2": 5,
            "test3": "string",
        },
    )
    resp_js = response.json()
    assert response.status_code == 200
    assert resp_js.get("session_token") is not None
    assert int(resp_js.get("expires")) is not None
    # Check which aditional data was saved
    usr = users_collection.find_one({"email": "user1@example.com"})
    # Check which data should be saved (testing_conf.json)
    assert usr.get("test") is True
    assert usr.get("test2") is None
    assert usr.get("test3") is None


# MISSING DATA TESTS
def test_create_account_missing_data():
    response = client.post(
        "/signup",
        json={"password": "Kennwort1!", "email": "user1@example.com"},
    )
    assert response.status_code == 422


# PASSWORD TESTS
def test_create_account_insecure_password_no_numbers():
    response = client.post(
        "/signup",
        json={
            "password": "Kennworts!",
            "email": "user1@example.com",
            "username": "TEST",
        },
    )
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, Make sure your password has a number in it"
    )
    assert response.status_code == 422


def test_create_account_insecure_password_too_long():
    response = client.post(
        "/signup",
        json={
            "password": "Kennworts!jaslkfdjasdlkfa12lsöjfdlksadjflkasjdflkjsadklfjsaldkfjsalkfdj",
            "email": "user1@example.com",
            "username": "TEST",
        },
    )
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, Make sure your password is at most 50 characters"
    )
    assert response.status_code == 422


def test_create_account_insecure_password_no_capital_case():
    response = client.post(
        "/signup",
        json={
            "password": "kennwort1!",
            "email": "user1@example.com",
            "username": "TEST",
        },
    )
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, Make sure your password has a capital letter in it"
    )
    assert response.status_code == 422


def test_create_account_insecure_password_no_special_character():
    response = client.post(
        "/signup",
        json={
            "password": "Kennwort123",
            "email": "user1@example.com",
            "username": "TEST",
        },
    )
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, Make sure your password has a special character in it"
    )
    assert response.status_code == 422


def test_create_account_insecure_password_multiple_problems():
    response = client.post(
        "/signup",
        json={
            "password": "sehrsicherespasswort",
            "email": "user1@example.com",
            "username": "TEST",
        },
    )
    assert response.status_code == 422


# USERNAME TESTS
def test_create_account_invalid_username_too_short():
    response = client.post(
        "/signup",
        json={
            "password": "Kennwort1!",
            "email": "user1@example.com",
            "username": "SAS",
        },
    )
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, Username must be at least 4 characters long"
    )
    assert response.status_code == 422


def test_create_account_invalid_username_special_cases():
    response = client.post(
        "/signup",
        json={
            "password": "Kennwort1!",
            "email": "user1@example.com",
            "username": "<div></div>",
        },
    )
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, Username must only contain letters and numbers"
    )
    assert response.status_code == 422


def test_create_account_invalid_username_too_long():
    response = client.post(
        "/signup",
        json={
            "password": "Kennwort1!",
            "email": "user1@example.com",
            "username": "adsjfölksajdflkasjdlkfjasdlkfjlksajdflöksajdfölkjsadfkjasölkfj",
        },
    )
    assert (
        response.json()["detail"][0]["msg"]
        == "Value error, Username must be at most 20 characters long"
    )
    assert response.status_code == 422


# INVALID EMAIL TESTS
def test_create_account_invalid_email():
    response = client.post(
        "/signup",
        json={
            "password": "Kennwort1!",
            "email": "user1example.com",
            "username": "TEST",
        },
    )
    assert "email" in response.json()["detail"][0]["msg"]
    assert response.status_code == 422


def test_create_account_invalid_email_2():
    response = client.post(
        "/signup",
        json={
            "password": "Kennwort1!",
            "email": "test@",
            "username": "TEST",
        },
    )
    assert (
        response.json()["detail"][0]["msg"]
        == "value is not a valid email address: There must be something after the @-sign."
    )
    assert response.status_code == 422
