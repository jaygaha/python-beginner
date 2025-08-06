import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Adjust imports to match the project structure
from main import app
from database.database import Base, get_db
from newsletter.schemas import NewsletterSubscriptionCreate

# 1. Test Database Setup
# Use an in-memory SQLite database for testing.
# `connect_args={"check_same_thread": False}` is needed for SQLite because
# each test runs in a different thread.
# `StaticPool` is used to ensure the same connection is used across the test session.
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 2. Dependency Override
# This function will override the `get_db` dependency in the main application.
# It ensures that during tests, we use the in-memory SQLite database instead of
# the production one configured in `.env`.
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Apply the dependency override to the FastAPI app.
app.dependency_overrides[get_db] = override_get_db


# 3. Test Fixture for Database Setup and Teardown
# A pytest fixture is a function that runs before each test function that uses it.
# This fixture sets up the database schema before a test runs and tears it down afterward.
# The `yield` statement passes control to the test function. After the test is done,
# the code after `yield` is executed. This ensures each test starts with a clean database.
@pytest.fixture(scope="function")
def db_session():
    # Create all database tables based on the models
    Base.metadata.create_all(bind=engine)
    yield
    # Drop all database tables after the test finishes
    Base.metadata.drop_all(bind=engine)


# 4. Test Client
# Create an instance of the TestClient, passing in our FastAPI app.
# This client allows us to make HTTP requests to the app within our tests
# without needing to run a live server.
client = TestClient(app)


# --- Test Cases ---

def test_subscribe_success(db_session):
    """
    Test Case 1: Successful Subscription
    - Description: Verifies that a user can subscribe with a valid email address.
    - Fixture `db_session`: This test uses the `db_session` fixture to ensure
      the database is clean before it runs.
    - Expected Outcome: The API should return a 200 OK status code and the
      created subscription object with the correct details.
    """
    response = client.post(
        "/newsletter/subscribe",
        json={"email": "test@example.com"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True
    assert "id" in data
    assert "created_at" in data


def test_subscribe_duplicate_email(db_session):
    """
    Test Case 2: Duplicate Email Subscription
    - Description: Verifies that the system prevents duplicate email subscriptions.
      It first subscribes an email and then attempts to subscribe the same email again.
    - Expected Outcome: The second request should fail with a 400 Bad Request
      status code and a specific error message.
    """
    # First subscription (should succeed)
    client.post("/newsletter/subscribe", json={"email": "duplicate@example.com"})

    # Second subscription with the same email (should fail)
    response = client.post(
        "/newsletter/subscribe",
        json={"email": "duplicate@example.com"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already subscribed"


def test_get_all_subscriptions(db_session):
    """
    Test Case 3: Retrieve All Subscriptions
    - Description: Verifies that the endpoint to get all subscriptions works correctly.
      It subscribes two different emails and then fetches the list.
    - Expected Outcome: The API should return a 200 OK status code and a list
      containing the two subscription objects created.
    """
    # Subscribe two different emails
    client.post("/newsletter/subscribe", json={"email": "user1@example.com"})
    client.post("/newsletter/subscribe", json={"email": "user2@example.com"})

    # Get all subscriptions
    response = client.get("/newsletter/subscriptions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "user1@example.com"
    assert data[1]["email"] == "user2@example.com"


def test_unsubscribe_success(db_session):
    """
    Test Case 4: Successful Unsubscription
    - Description: Verifies that a user can successfully unsubscribe. It subscribes
      an email and then immediately sends a request to delete it.
    - Expected Outcome: The delete request should return a 200 OK status code with
      a success message. A follow-up check ensures the subscription list is empty.
    """
    email_to_unsubscribe = "unsubscribe@example.com"
    # Subscribe an email first
    client.post("/newsletter/subscribe", json={"email": email_to_unsubscribe})

    # Unsubscribe the email
    response = client.delete(f"/newsletter/unsubscribe/{email_to_unsubscribe}")
    assert response.status_code == 200
    assert response.json()["message"] == "Successfully unsubscribed"

    # Verify the subscription is actually gone by fetching all subscriptions
    get_response = client.get("/newsletter/subscriptions")
    assert len(get_response.json()) == 0


def test_unsubscribe_not_found(db_session):
    """
    Test Case 5: Unsubscribing a Non-existent Email
    - Description: Verifies that attempting to unsubscribe an email that is not
      in the database fails gracefully.
    - Expected Outcome: The API should return a 404 Not Found status code with
      a specific error message.
    """
    non_existent_email = "notfound@example.com"
    response = client.delete(f"/newsletter/unsubscribe/{non_existent_email}")
    assert response.status_code == 404
    assert response.json()["detail"] == "Subscription not found"
