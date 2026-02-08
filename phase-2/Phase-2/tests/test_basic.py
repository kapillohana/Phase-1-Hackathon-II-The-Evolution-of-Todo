from fastapi.testclient import TestClient
from backend.src.main import app

def test_health_check():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"

def test_api_docs():
    client = TestClient(app)
    response = client.get("/docs")
    assert response.status_code == 200

def test_root_endpoint():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "status" in data