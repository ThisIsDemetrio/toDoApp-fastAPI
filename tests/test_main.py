from fastapi.testclient import TestClient
from fastapi import status

from main import app

client = TestClient(app)


def test_check_health_route():
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "OK"}


def test_check_db_health_route():
    response = client.get("/db-health")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "OK"
    assert response.json()["existingConfigs"] == 0
