"""Tests for API endpoints"""

import pytest
from fastapi.testclient import TestClient
from src.api import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app()
    return TestClient(app)


def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert "status" in response.json()
    assert response.json()["status"] == "ok"


def test_agents_endpoint(client):
    """Test agents list endpoint"""
    response = client.get("/agents")
    assert response.status_code == 200
    data = response.json()
    assert "single_agent" in data
    assert "multi_agents" in data
    assert "usage" in data


def test_chat_endpoint_missing_message(client):
    """Test chat endpoint with missing message"""
    response = client.post("/chat", json={"message": ""})
    assert response.status_code == 400


def test_invalid_file_upload(client):
    """Test file upload with invalid file type"""
    data = {
        "file": ("test.exe", b"fake content", "application/octet-stream")
    }
    response = client.post("/upload", files=data)
    assert response.status_code == 400
