import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "smart-city-big-data-backend"
    assert "version" in data

def test_system_info():
    response = client.get("/api/system/info")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "smart-city-big-data-backend"
    assert "version" in data
    assert "environment" in data
