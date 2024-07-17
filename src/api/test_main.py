from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_read_up():
    response = client.get("/up")
    assert response.status_code == 204


def test_read_docs():
    response = client.get("/docs")
    assert response.status_code == 200


def test_redirect_home():
    response = client.get("/")
    assert response.status_code == 200
    assert "docs" in response.url.path
