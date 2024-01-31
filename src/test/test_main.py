from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app=app)


def test_read_main():
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}
