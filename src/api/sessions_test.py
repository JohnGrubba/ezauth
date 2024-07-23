from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


# SUCCESSFUL TESTS
def test_get_sessions(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.get("/sessions")
    resp_js = response.json()
    assert response.status_code == 200
    assert isinstance(resp_js.get("sessions"), list)
    assert len(resp_js.get("sessions")) == 1
    # Don't leak out session_token
    assert resp_js.get("sessions")[0].get("session_token") is None


def test_delete_session(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.delete("/sessions/" + str(fixturesessiontoken_user[2]))
    assert response.status_code == 204


def test_delete_session_otheracc(fixturesessiontoken_user, fixturesessiontoken_user2):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.delete("/sessions/" + str(fixturesessiontoken_user2[2]))
    assert response.status_code == 404


def test_delete_session_nonexistent(fixturesessiontoken_user):
    client.cookies.set("session", fixturesessiontoken_user[0])
    response = client.delete("/sessions/test")
    assert response.status_code == 404
