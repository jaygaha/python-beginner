import pytest
from pydantic import ValidationError
from datetime import datetime
from src.enums.user_enum import UserStatus
from src.models.user import UserBase, UserCreate, UserResponse, UserUpdate, UsersListResponse

def test_user_base_valid():
    user = UserBase(
        username="testuser",
        email="test@example.com",
        age=25,
        status=UserStatus.ACTIVE,
        full_name="Test User"
    )
    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.age == 25
    assert user.status == UserStatus.ACTIVE
    assert user.full_name == "Test User"

def test_user_base_invalid_email():
    with pytest.raises(ValidationError):
        UserBase(
            username="testuser",
            email="invalid-email",
            age=25,
            status=UserStatus.ACTIVE
        )

def test_user_base_invalid_age():
    with pytest.raises(ValidationError):
        UserBase(
            username="testuser",
            email="test@example.com",
            age=-1,
            status=UserStatus.ACTIVE
        )
    with pytest.raises(ValidationError):
        UserBase(
            username="testuser",
            email="test@example.com",
            age=121,
            status=UserStatus.ACTIVE
        )

def test_user_base_username_length():
    with pytest.raises(ValidationError):
        UserBase(
            username="ab",  # Too short
            email="test@example.com",
            age=25,
            status=UserStatus.ACTIVE
        )
    with pytest.raises(ValidationError):
        UserBase(
            username="a" * 101,  # Too long
            email="test@example.com",
            age=25,
            status=UserStatus.ACTIVE
        )

def test_user_create_valid():
    user = UserCreate(
        username="testuser",
        email="test@example.com",
        age=25,
        status=UserStatus.ACTIVE,
        password="securepassword123"
    )
    assert user.password == "securepassword123"
    assert isinstance(user, UserBase)

def test_user_create_invalid_password():
    with pytest.raises(ValidationError):
        UserCreate(
            username="testuser",
            email="test@example.com",
            age=25,
            status=UserStatus.ACTIVE,
            password="short"  # Too short
        )

def test_user_response_valid():
    user = UserResponse(
        id=1,
        username="testuser",
        email="test@example.com",
        age=25,
        status=UserStatus.ACTIVE,
        is_active=True,
        created_at=datetime.now()
    )
    assert user.id == 1
    assert user.is_active is True
    assert isinstance(user.created_at, datetime)

def test_user_response_from_dict():
    data = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "age": 25,
        "status": "active",
        "is_active": True,
        "created_at": "2023-01-01T12:00:00"
    }
    user = UserResponse(**data)
    assert user.status == UserStatus.ACTIVE
    assert user.created_at == datetime.fromisoformat("2023-01-01T12:00:00")

def test_user_update_valid():
    user = UserUpdate(
        username="newuser",
        email="new@example.com",
        full_name="New Name"
    )
    assert user.username == "newuser"
    assert user.email == "new@example.com"
    assert user.full_name == "New Name"

def test_user_update_partial():
    user = UserUpdate(
        email="new@example.com"
    )
    assert user.email == "new@example.com"
    assert user.username is None
    assert user.full_name is None

def test_user_update_invalid_email():
    with pytest.raises(ValidationError):
        UserUpdate(email="invalid-email")

def test_users_list_response_valid():
    user_response = UserResponse(
        id=1,
        username="testuser",
        email="test@example.com",
        age=25,
        status=UserStatus.ACTIVE,
        is_active=True,
        created_at=datetime.now()
    )
    users_list = UsersListResponse(
        users=[user_response],
        total=1,
        skip=0,
        limit=10
    )
    assert len(users_list.users) == 1
    assert users_list.total == 1
    assert users_list.skip == 0
    assert users_list.limit == 10
