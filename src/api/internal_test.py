from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)

client.headers = {"internal-api-key": "TEST_INTERNAL"}


# Unauthorized Route Test
def test_unauthorized_internal_ping():
    # Test multiple endpoints (to ensure every /internal endpoint is protected)
    response = client.get("/internal/health", headers={"internal-api-key": ""})
    assert response.status_code == 401
    response = client.post("/internal/users", headers={"internal-api-key": ""})
    assert response.status_code == 401
    response = client.post("/internal/profile", headers={"internal-api-key": ""})
    assert response.status_code == 401


# SUCCESSFUL TESTS
def test_internal_ping():
    response = client.get("/internal/health")
    resp_js = response.json()
    assert response.status_code == 200
    assert resp_js.get("status") == "ok"


def test_internal_profile(fixtureuser):
    response = client.post(
        "/internal/profile",
        json={"user_id": fixtureuser["_id"]},
    )
    resp_js = response.json()
    assert response.status_code == 200
    assert resp_js.get("email") == fixtureuser["email"]


def test_batch_profiles(fixtureuser, fixtureuser2):
    response = client.get(
        "/internal/batch-users",
        params={"user_ids_req": f'{fixtureuser["_id"]},{fixtureuser2["_id"]}'},
    )
    resp_js = response.json()
    assert response.status_code == 200
    assert len(resp_js) == 2
    assert resp_js[0].get("email") == fixtureuser["email"]
