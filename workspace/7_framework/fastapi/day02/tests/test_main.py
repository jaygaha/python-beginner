import pytest
from fastapi.testclient import TestClient
from src.main import app, users_db

# TestClient allows us to make requests to our FastAPI app in tests.
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    """
    This is a pytest fixture. It runs before each test function.
    It ensures that our 'database' is empty before every single test,
    so that tests don't interfere with each other.
    """
    global users_db, next_id
    users_db.clear()
    next_id = 1
    yield
    # Code after 'yield' would run after each test, but we don't need it here.

# A sample user payload we can reuse in our tests.
USER_PAYLOAD = {
    "username": "testuser",
    "email": "test@example.com",
    "full_name": "Test User",
    "password": "a_strong_password",
    "age": 30
}

def test_create_user():
    """Test the successful creation of a user."""
    # Action: Make a POST request to create a user.
    response = client.post("/users", json=USER_PAYLOAD)

    # Assertions: Check if the outcome is what we expect.
    assert response.status_code == 201 # 201 Created
    data = response.json()
    assert data["email"] == USER_PAYLOAD["email"]
    assert data["username"] == USER_PAYLOAD["username"]
    assert "id" in data
    assert "password" not in data # Ensure password is not returned.
    assert users_db[0]["id"] == 1 # Check if it's actually in our DB.

def test_get_users():
    """Test retrieving a list of all users."""
    # Setup: Create a user first.
    client.post("/users", json=USER_PAYLOAD)

    # Action: Make a GET request to the users list endpoint.
    response = client.get("/users")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["username"] == USER_PAYLOAD["username"]

def test_get_user_by_id_success():
    """Test retrieving a single user by ID when they exist."""
    # Setup: Create a user to get its ID.
    create_response = client.post("/users", json=USER_PAYLOAD)
    user_id = create_response.json()["id"]

    # Action: Request the user by its ID.
    response = client.get(f"/users/{user_id}")

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == USER_PAYLOAD["email"]

def test_get_user_by_id_not_found():
    """Test retrieving a user that does not exist."""
    # Action: Request a user ID that we know doesn't exist.
    response = client.get("/users/999")

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_update_user_success():
    """Test successfully updating a user's information."""
    # Setup: Create a user.
    create_response = client.post("/users", json=USER_PAYLOAD)
    user_id = create_response.json()["id"]

    update_payload = {"full_name": "Updated Test User", "username": "new_username"}

    # Action: Make a PUT request to update the user.
    response = client.put(f"/users/{user_id}", json=update_payload)

    # Assertions
    assert response.status_code == 200
    data = response.json()
    assert data["full_name"] == "Updated Test User"
    assert data["username"] == "new_username"
    # Ensure other data was not changed
    assert data["email"] == USER_PAYLOAD["email"]

def test_update_user_not_found():
    """Test updating a user that does not exist."""
    # Action
    response = client.put("/users/999", json={"username": "ghost"})

    # Assertions
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}
