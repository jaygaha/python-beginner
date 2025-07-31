import pytest_asyncio
from fastapi.testclient import TestClient
from datetime import datetime
from src.main import app, users_db
from src.enums.user_enum import UserStatus

# Create a test client for the FastAPI app
client = TestClient(app)

# Fixture to reset the in-memory database before each test
@pytest_asyncio.fixture(autouse=True)
async def reset_db():
    global users_db, next_id
    users_db.clear()
    users_db.extend([
        {
            "id": 1,
            "username": "code.conductor",
            "email": "jay@example.com",
            "full_name": "Jay",
            "age": 25,
            "status": UserStatus.ACTIVE,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "id": 2,
            "username": "jane.smith",
            "email": "jane@example.com",
            "full_name": "Jane Smith",
            "age": 12,
            "status": UserStatus.INACTIVE,
            "is_active": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "id": 3,
            "username": "alice.johnson",
            "email": "alice@example.com",
            "full_name": "Alice Johnson",
            "age": 28,
            "status": UserStatus.ACTIVE,
            "is_active": True,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
        {
            "id": 4,
            "username": "bob.smith",
            "email": "bob@example.com",
            "full_name": "Bob Smith",
            "age": 35,
            "status": UserStatus.SUSPENDED,
            "is_active": False,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        },
    ])
    global next_id
    next_id = 5
    yield

def test_create_user_valid():
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "age": 30,
        "status": "active",
        "password": "securepassword123"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 201
    assert response.json()["username"] == "newuser"
    assert response.json()["email"] == "newuser@example.com"
    assert response.json()["age"] == 30
    assert response.json()["status"] == "active"
    assert response.json()["is_active"] is True
    assert "password" not in response.json()
    assert "id" in response.json()
    assert response.json()["id"] == 5

def test_create_user_invalid_email():
    user_data = {
        "username": "newuser",
        "email": "invalid-email",
        "age": 30,
        "status": "active",
        "password": "securepassword123"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422

def test_create_user_invalid_status():
    user_data = {
        "username": "newuser",
        "email": "newuser@example.com",
        "age": 30,
        "status": "invalid",
        "password": "securepassword123"
    }
    response = client.post("/users", json=user_data)
    assert response.status_code == 422

def test_get_users_all():
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 4
    assert len(data["users"]) == 4
    assert data["skip"] == 0
    assert data["limit"] == 10
    assert data["users"][0]["username"] == "code.conductor"

def test_get_users_with_pagination():
    response = client.get("/users?skip=1&limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 4
    assert len(data["users"]) == 2
    assert data["users"][0]["username"] == "jane.smith"
    assert data["users"][1]["username"] == "alice.johnson"
    assert data["skip"] == 1
    assert data["limit"] == 2

def test_get_users_with_status_filter():
    response = client.get("/users?status=active")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["users"]) == 2
    assert all(user["status"] == "active" for user in data["users"])

def test_get_users_with_age_filter():
    response = client.get("/users?min_age=20&max_age=30")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["users"]) == 2
    assert all(20 <= user["age"] <= 30 for user in data["users"])

def test_get_users_with_search():
    response = client.get("/users?search=smith")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert len(data["users"]) == 2
    assert all("Smith" in user["full_name"] for user in data["users"])

def test_get_users_with_sort():
    response = client.get("/users?sort_by=age&sort_order=desc")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 4
    assert len(data["users"]) == 4
    assert data["users"][0]["age"] == 35
    assert data["users"][1]["age"] == 28

def test_get_users_with_include_age():
    response = client.get("/users?include_age=true")
    assert response.status_code == 200
    data = response.json()
    assert all("age" in user for user in data["users"])

def test_get_users_invalid_sort_by():
    response = client.get("/users?sort_by=invalid_field")
    assert response.status_code == 422

def test_get_user_by_id_valid():
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["username"] == "code.conductor"
    assert data["email"] == "jay@example.com"

def test_get_user_by_id_not_found():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_update_user_valid():
    update_data = {
        "username": "updateduser",
        "email": "updated@example.com",
        "full_name": "Updated Name"
    }
    response = client.put("/users/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "updateduser"
    assert data["email"] == "updated@example.com"
    assert data["full_name"] == "Updated Name"
    assert data["id"] == 1

def test_update_user_partial():
    update_data = {
        "email": "newemail@example.com"
    }
    response = client.put("/users/1", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newemail@example.com"
    assert data["username"] == "code.conductor"  # Unchanged
    assert data["id"] == 1

def test_update_user_not_found():
    update_data = {
        "username": "updateduser"
    }
    response = client.put("/users/999", json=update_data)
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_update_user_invalid_email():
    update_data = {
        "email": "invalid-email"
    }
    response = client.put("/users/1", json=update_data)
    assert response.status_code == 422
