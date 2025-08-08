import pytest
from fastapi.testclient import TestClient

def get_auth_headers(client: TestClient, test_user_data):
    """Helper function to get authentication headers"""
    response = client.post("/api/v1/auth/register", data=test_user_data)
    tokens = response.json()
    return {"Authorization": f"Bearer {tokens['access_token']}"}

def test_get_current_user(client: TestClient, test_user_data):
    """Test getting current user profile"""
    headers = get_auth_headers(client, test_user_data)

    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_data["username"]
    assert data["email"] == test_user_data["email"]
    assert "id" in data

def test_get_current_user_unauthorized(client: TestClient):
    """Test getting current user without authentication"""
    response = client.get("/api/v1/users/me")
    assert response.status_code == 401

def test_get_current_user_invalid_token(client: TestClient):
    """Test getting current user with invalid token"""
    headers = {"Authorization": "Bearer invalid_token"}
    response = client.get("/api/v1/users/me", headers=headers)
    assert response.status_code == 401

def test_update_current_user(client: TestClient, test_user_data):
    """Test updating current user profile"""
    headers = get_auth_headers(client, test_user_data)

    update_data = {
        "username": "updateduser",
        "email": "updated@example.com"
    }
    response = client.put("/api/v1/users/me", json=update_data, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"
    assert data["email"] == "updated@example.com"

def test_admin_endpoint_as_regular_user(client: TestClient, test_user_data):
    """Test accessing admin endpoint as regular user"""
    headers = get_auth_headers(client, test_user_data)

    response = client.get("/api/v1/users/admin-only", headers=headers)
    assert response.status_code == 403
