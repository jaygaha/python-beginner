import pytest
from fastapi.testclient import TestClient
from src.main import app, items_db, users_db
from fastapi import status
import hashlib

# Fixture to provide a test client for the app.
# The scope is 'module' so it's created only once per test module.
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client

# Fixture to reset the database state before each test.
# 'autouse=True' ensures it runs automatically for every test, providing isolation.
@pytest.fixture(autouse=True)
def reset_db():
    # Reset items_db to its original state
    items_db[:] = [
        {"id": 1, "name": "Item 1", "price": 10.0, "is_active": True, "owner_id": 1},
        {"id": 2, "name": "Item 2", "price": 20.0, "is_active": False, "owner_id": 2},
        {"id": 3, "name": "Item 3", "price": 15.0, "is_active": True, "owner_id": 1},
    ]
    # Reset and repopulate users_db
    users_db.clear()
    users_db["testuser"] = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "hashed_password": hashlib.sha256("testpassword".encode()).hexdigest(),
        "roles": [],
        "is_active": True
    }
    users_db["adminuser"] = {
        "id": 2,
        "username": "adminuser",
        "email": "admin@example.com",
        "hashed_password": hashlib.sha256("adminpassword".encode()).hexdigest(),
        "roles": ["admin"],
        "is_active": True
    }

# Helper function to get an authentication header with a token
def get_auth_header(client, username="testuser", password="testpassword"):
    response = client.post("/token", data={"username": username, "password": password})
    assert response.status_code == status.HTTP_200_OK, "Failed to get token"
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# --- Test Cases ---

def test_get_token_success(client):
    """Test successful token generation for a valid user."""
    response = client.post("/token", data={"username": "testuser", "password": "testpassword"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_token_failure(client):
    """Test token generation fails for invalid credentials."""
    response = client.post("/token", data={"username": "testuser", "password": "wrongpassword"})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_read_current_user(client):
    """Test fetching the current authenticated user's data."""
    headers = get_auth_header(client)
    response = client.get("/users/me", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"] == "testuser"

def test_get_all_items(client):
    """Test fetching all items (including inactive) for an authenticated user."""
    headers = get_auth_header(client)
    response = client.get("/items/?include_inactive=true", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert "items" in response.json()
    assert len(response.json()["items"]) == 3

def test_get_single_item(client):
    """Test fetching a single item by its ID."""
    headers = get_auth_header(client)
    response = client.get("/items/1", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["item"]["id"] == 1

def test_get_item_not_found(client):
    """Test that fetching a non-existent item results in a 404 error."""
    headers = get_auth_header(client)
    response = client.get("/items/99", headers=headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_create_item(client):
    """Test creating a new item."""
    headers = get_auth_header(client)
    item_data = {"name": "New Test Item", "price": 99.99}
    response = client.post("/items/", json=item_data, headers=headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["item"]["name"] == item_data["name"]
    assert data["created_by"] == "testuser"
    assert len(items_db) == 4

def test_delete_item(client):
    """Test deleting an item owned by the user."""
    headers = get_auth_header(client, "adminuser", "adminpassword")
    response = client.delete("/items/2", headers=headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Item deleted successfully"
    assert len(items_db) == 2

def test_admin_access_required(client):
    """Test that a non-admin user cannot access admin-only endpoints."""
    headers = get_auth_header(client) # Regular user
    response = client.get("/admin/users", headers=headers)
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_admin_can_get_all_users(client):
    """Test that an admin user can fetch all users."""
    admin_headers = get_auth_header(client, "adminuser", "adminpassword")
    response = client.get("/admin/users", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["users"]) == 2

def test_admin_can_activate_item(client):
    """Test that an admin can activate an inactive item."""
    admin_headers = get_auth_header(client, "adminuser", "adminpassword")
    # Item with ID 2 is initially inactive
    assert items_db[1]["is_active"] is False
    response = client.post("/admin/items/2/activate", headers=admin_headers)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["item"]["is_active"] is True
