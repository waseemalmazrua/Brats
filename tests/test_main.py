from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.main import app




def test_read_main(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok 200"}