from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_check_health_route():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "OK"}


def test_check_db_health_route():
    response = client.get("/db-health")
    assert response.status_code == 200
    assert response.json()["status"] == "OK"
    assert response.json()["existingConfigs"] == 0
