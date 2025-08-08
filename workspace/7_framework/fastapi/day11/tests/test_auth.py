import pytest
from fastapi.testclient import TestClient
from src.services.auth_service import AuthService

def test_register_user(client: TestClient, test_user_data):
    """Test user registration"""
    response = client.post("/api/v1/auth/register", data=test_user_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_register_duplicate_user(client: TestClient, test_user_data):
    """Test registration with duplicate username"""
    # Register first user
    client.post("/api/v1/auth/register", data=test_user_data)

    # Try to register same user again
    response = client.post("/api/v1/auth/register", data=test_user_data)
    assert response.status_code == 400
    assert "Username already registered" in response.json()["detail"]

def test_login_user(client: TestClient, test_user_data):
    """Test user login"""
    # Register user first
    client.post("/api/v1/auth/register", data=test_user_data)

    # Login
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials"""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401

def test_refresh_token(client: TestClient, test_user_data):
    """Test token refresh"""
    # Register and get tokens
    register_response = client.post("/api/v1/auth/register", data=test_user_data)
    tokens = register_response.json()

    # Refresh token
    refresh_data = {"refresh_token": tokens["refresh_token"]}
    response = client.post("/api/v1/auth/refresh", json=refresh_data)
    assert response.status_code == 200
    new_tokens = response.json()
    assert "access_token" in new_tokens
    assert "refresh_token" in new_tokens

def test_auth_service_authenticate_user(db, created_user):
    """Test AuthService authenticate_user method"""
    auth_service = AuthService(db)

    # Test successful authentication
    result = auth_service.authenticate_user("testuser", "testpassword123")
    assert result is not None
    assert result["username"] == "testuser"

    # Test failed authentication
    result = auth_service.authenticate_user("testuser", "wrongpassword")
    assert result is None
