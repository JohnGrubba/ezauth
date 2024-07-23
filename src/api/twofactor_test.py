from fastapi.testclient import TestClient
import pytest
import pyotp

from .main import app

client = TestClient(app)


# Request 2FA
@pytest.fixture
def request2fa_fixture(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.post("/2fa/enable")
    resp_js = response.json()
    return resp_js["provision_uri"]


def test_request_2fa(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.post("/2fa/enable")
    resp_js = response.json()
    assert response.status_code == 200
    assert resp_js["provision_uri"] is not None


def test_request_2fa_qr(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.get("/2fa/enable")
    assert response.status_code == 200
    assert response.headers.get("Content-Type") == "image/svg+xml"


# Enable 2FA
def test_enable_2fa_prov_url(fixturesessiontoken_user, request2fa_fixture):
    otp_instance: pyotp.TOTP = pyotp.parse_uri(request2fa_fixture)
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.post("/2fa/confirm-enable", json={"code": otp_instance.now()})
    assert response.status_code == 204


def test_enable_2fa_prov_url_invalid_code(fixturesessiontoken_user, request2fa_fixture):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.post("/2fa/confirm-enable", json={"code": 123456})
    assert response.status_code == 400


def test_request_2fa_no_login(fixturesessiontoken_user):
    response = client.post("/2fa/enable")
    assert response.status_code == 401


def test_request_2fa_no_login_qr(fixturesessiontoken_user):
    response = client.get("/2fa/enable")
    assert response.status_code == 401
