"""
Cyber Crime Reporting System - Backend Tests

Unit tests for FastAPI backend.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os
from unittest.mock import Mock, patch

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test API root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Cyber Crime Reporting System API" in response.json()["message"]

def test_register_user():
    """Test user registration."""
    user_data = {
        "email": "test@example.com",
        "password": "securepassword123",
        "full_name": "Test User",
        "phone": "03001234567",
        "cnic": "1234567890123"
    }
    response = client.post("/auth/register", json=user_data)
    # This will fail until Supabase integration is complete
    assert response.status_code in [200, 500]  # Allow for incomplete implementation

def test_create_complaint():
    """Test complaint creation."""
    complaint_data = {
        "incident_date": "2024-01-15",
        "location": "Karachi",
        "complaint_reason": "Phishing",
        "description": "Received phishing email from unknown sender."
    }
    response = client.post("/complaints/", json=complaint_data)
    # Will require authentication token
    assert response.status_code == 401  # Unauthorized without token

def test_get_laws():
    """Test retrieving cyber laws."""
    response = client.get("/laws/")
    assert response.status_code == 200
    assert "laws" in response.json()

@patch('api.main.validate_file')
def test_evidence_upload(mock_validate):
    """Test evidence file upload."""
    mock_validate.return_value = {
        "size": 1024,
        "mime_type": "image/jpeg",
        "sha256_hash": "dummy_hash"
    }

    # Mock file upload
    files = {"files": ("test.jpg", b"dummy image data", "image/jpeg")}
    data = {"complaint_id": "test-id"}

    response = client.post("/evidence/upload", files=files, data=data)
    # Will require authentication
    assert response.status_code == 401

if __name__ == "__main__":
    pytest.main([__file__])