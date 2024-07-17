from fastapi.testclient import TestClient
from tools import users_collection

from .main import app

client = TestClient(app)


def test_create_account():
    print("SAS")
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
