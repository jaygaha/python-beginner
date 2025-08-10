from fastapi import APIRouter, HTTPException, Query, Path, Body, status
from fastapi.responses import JSONResponse
from typing import List, Optional
from src.models.schemas import (
    UserCreate, UserResponse, UserUpdate, ErrorResponse, ValidationErrorResponse
)

router = APIRouter(prefix="/api/v1/users", tags=["users"])

# Mock database
fake_users_db = [
    {
        "id": 1,
        "email": "john.doe@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "role": "customer",
        "is_active": True,
        "created_at": "2023-01-01T00:00:00"
    },
    {
        "id": 2,
        "email": "admin@example.com",
        "first_name": "Admin",
        "last_name": "User",
        "role": "admin",
        "is_active": True,
        "created_at": "2023-01-01T00:00:00"
    }
]


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="Get all users",
    description="Retrieve a paginated list of all users in the system.",
    response_description="List of users with pagination",
    responses={
        200: {
            "description": "Successful response",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "email": "john.doe@example.com",
                            "first_name": "John",
                            "last_name": "Doe",
                            "role": "customer",
                            "is_active": True,
                            "created_at": "2023-01-01T00:00:00"
                        }
                    ]
                }
            }
        }
    }
)
async def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip for pagination", examples=[0]),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of users to return", examples=[10]),
    role: Optional[str] = Query(None, description="Filter users by role", examples=["customer"])
):
    """
    Get a paginated list of users with optional role filtering.

    - **skip**: Number of users to skip (for pagination)
    - **limit**: Maximum number of users to return (1-100)
    - **role**: Optional role filter (customer, admin, moderator)
    """
    users = fake_users_db.copy()

    if role:
        users = [user for user in users if user["role"] == role]

    return users[skip:skip + limit]


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user by ID",
    description="Retrieve a specific user by their unique identifier.",
    responses={
        200: {
            "description": "User found successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "email": "john.doe@example.com",
                        "first_name": "John",
                        "last_name": "Doe",
                        "role": "customer",
                        "is_active": True,
                        "created_at": "2023-01-01T00:00:00"
                    }
                }
            }
        },
        404: {
            "description": "User not found",
            "model": ErrorResponse,
            "content": {
                "application/json": {
                    "example": {
                        "detail": "User not found",
                        "error_code": "USER_NOT_FOUND"
                    }
                }
            }
        }
    }
)
async def get_user(
    user_id: int = Path(..., gt=0, description="The unique identifier of the user", examples=[1])
):
    """
    Get a specific user by ID.

    Returns detailed information about a user including their profile data and account status.
    """
    user = next((user for user in fake_users_db if user["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
    description="Create a new user account with the provided information.",
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {
                        "id": 3,
                        "email": "new.user@example.com",
                        "first_name": "New",
                        "last_name": "User",
                        "role": "customer",
                        "is_active": True,
                        "created_at": "2023-11-01T10:30:00"
                    }
                }
            }
        },
        422: {
            "description": "Validation error",
            "model": ValidationErrorResponse
        }
    }
)
async def create_user(user: UserCreate):
    """
    Create a new user account.

    **Required fields:**
    - email: Must be a valid email address
    - first_name: 1-50 characters
    - last_name: 1-50 characters
    - password: Minimum 8 characters with uppercase, lowercase, and digit

    **Optional fields:**
    - role: Defaults to 'customer'
    """
    # Check if email already exists
    if any(u["email"] == user.email for u in fake_users_db):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    new_user = {
        "id": len(fake_users_db) + 1,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "role": user.role,
        "is_active": True,
        "created_at": "2023-11-01T10:30:00"
    }
    fake_users_db.append(new_user)
    return new_user


@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user",
    description="Update an existing user's information.",
    responses={
        200: {"description": "User updated successfully"},
        404: {"description": "User not found", "model": ErrorResponse}
    }
)
async def update_user(
    user_id: int = Path(..., gt=0, description="The unique identifier of the user to update"),
    user_update: UserUpdate = Body(...)
):
    """Update an existing user's information."""
    user_index = next((i for i, user in enumerate(fake_users_db) if user["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update user data
    user_data = fake_users_db[user_index].copy()
    update_data = user_update.dict(exclude_unset=True)
    user_data.update(update_data)
    fake_users_db[user_index] = user_data

    return user_data


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete user",
    description="Delete a user account permanently.",
    responses={
        204: {"description": "User deleted successfully"},
        404: {"description": "User not found", "model": ErrorResponse}
    }
)
async def delete_user(
    user_id: int = Path(..., gt=0, description="The unique identifier of the user to delete")
):
    """
    Delete a user account permanently.

    ⚠️ **Warning**: This action cannot be undone!
    """
    user_index = next((i for i, user in enumerate(fake_users_db) if user["id"] == user_id), None)
    if user_index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    fake_users_db.pop(user_index)
    return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
