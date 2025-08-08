import os
os.environ["DISABLE_BACKGROUND_JOBS"] = "1"

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_metrics_endpoints():
    resp_all = client.get("/models/metrics")
    assert resp_all.status_code == 200
    resp_one = client.get("/models/metrics/gold")
    assert resp_one.status_code == 200