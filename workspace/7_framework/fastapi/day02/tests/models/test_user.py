import pytest
from pydantic import ValidationError
from src.models.user import UserCreate, UserUpdate

# A pytest fixture to provide valid user data for tests.
# This avoids repeating the same dictionary in every test.
@pytest.fixture
def valid_user_data():
    return {
        "username": "testuser",
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "a_strong_password",
        "age": 30
    }

def test_user_create_success(valid_user_data):
    """Tests successful creation of a UserCreate model with valid data."""
    try:
        user = UserCreate(**valid_user_data)
        assert user.username == valid_user_data["username"]
        assert user.email == valid_user_data["email"]
        assert user.age == 30
    except ValidationError as e:
        pytest.fail(f"Validation failed unexpectedly: {e}")

def test_username_too_short(valid_user_data):
    """Tests that a username shorter than 3 characters raises a ValidationError."""
    invalid_data = valid_user_data.copy()
    invalid_data["username"] = "ab" # Too short

    # 'pytest.raises' is the proper way to test for expected exceptions.
    # The 'with' block will pass only if a ValidationError is raised.
    with pytest.raises(ValidationError) as excinfo:
        UserCreate(**invalid_data)

    # Optionally, you can assert details about the error.
    assert "username" in str(excinfo.value)

def test_invalid_email(valid_user_data):
    """Tests that a malformed email raises a ValidationError."""
    invalid_data = valid_user_data.copy()
    invalid_data["email"] = "not-a-valid-email"

    with pytest.raises(ValidationError) as excinfo:
        UserCreate(**invalid_data)

    assert "email" in str(excinfo.value)

def test_age_out_of_bounds(valid_user_data):
    """Tests that an age outside the range 0-120 raises a ValidationError."""
    # Test age too high
    invalid_data_high = valid_user_data.copy()
    invalid_data_high["age"] = 130
    with pytest.raises(ValidationError):
        UserCreate(**invalid_data_high)

    # Test age too low
    invalid_data_low = valid_user_data.copy()
    invalid_data_low["age"] = -1
    with pytest.raises(ValidationError):
        UserCreate(**invalid_data_low)

def test_password_too_short(valid_user_data):
    """Tests that a password shorter than 8 characters raises a ValidationError."""
    invalid_data = valid_user_data.copy()
    invalid_data["password"] = "short" # Too short

    with pytest.raises(ValidationError):
        UserCreate(**invalid_data)

def test_user_update_allows_partial_data():
    """Tests that the UserUpdate model accepts partial data without errors."""
    try:
        # Should work with only one field
        update = UserUpdate(username="newname")
        assert update.username == "newname"
        assert update.email is None

        # Should work with no fields
        update_empty = UserUpdate()
        assert update_empty.model_dump(exclude_unset=True) == {}

    except ValidationError as e:
        pytest.fail(f"UserUpdate failed with valid partial data: {e}")
