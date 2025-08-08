import os
# Disable background tasks and schedulers for tests BEFORE importing app
os.environ["DISABLE_BACKGROUND_JOBS"] = "1"

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    data = resp.json()
    assert data.get("status") == "running"


def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert "status" in data


def test_stats_keys():
    resp = client.get("/stats")
    assert resp.status_code == 200
    data = resp.json()
    assert "total_price_records" in data
    assert "supported_commodities" in data