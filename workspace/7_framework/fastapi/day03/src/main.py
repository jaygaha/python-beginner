from fastapi import FastAPI, Path, Query, HTTPException
from models.user import UserCreate, UserResponse, UserUpdate, UsersListResponse
from enums.user_enum import UserStatus, SortOrder
from datetime import datetime
from typing import List, Dict, Any, Optional

app = FastAPI(title="User Management API", version="1.0.0")

# In-memory database - a simple list to store our user records.
# In a real app, this would be a database like PostgreSQL or MongoDB.
users_db: List[Dict[str, Any]] = [
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
]
next_id = 5

def _find_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    """Helper function to find a user in the 'database' by their ID."""
    for user in users_db:
        if user["id"] == user_id:
            return user
    return None

@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    """Creates a new user and adds them to the database."""
    global next_id

    new_user_data = user.model_dump()
    new_user_data.pop('password')
    new_user_data["id"] = next_id
    new_user_data["created_at"] = datetime.now()
    new_user_data["updated_at"] = datetime.now()
    new_user_data["is_active"] = True
    new_user_data["status"] = user.status

    users_db.append(new_user_data)
    next_id += 1

    return new_user_data

@app.get("/users", response_model=UsersListResponse)
def get_users(
    skip: int = Query(0, ge=0, description="Number of users to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of users to return"),
    status: Optional[UserStatus] = Query(None, description="Filter by status"),
    min_age: Optional[float] = Query(None, ge=0, description="Minimum age filter"),
    max_age: Optional[float] = Query(None, ge=0, description="Maximum age filter"),
    include_age: bool = Query(False, description="Include age in response"),
    search: Optional[str] = Query(None, min_length=1, max_length=50, description="Search in user names"),
    sort_by: str = Query("id", pattern="^(id|full_name|age|created_at)$"),
    sort_order: SortOrder = Query(SortOrder.ASC)
):
    """Returns a list of all users in the database."""
    filtered_users = users_db

    if status:
        filtered_users = [user for user in filtered_users if user["status"] == status]
    if min_age is not None:
        filtered_users = [user for user in filtered_users if user["age"] >= min_age]
    if max_age is not None:
        filtered_users = [user for user in filtered_users if user["age"] <= max_age]
    if search:
        filtered_users = [user for user in filtered_users if search.lower() in user["full_name"].lower()]

    reverse_order = sort_order == SortOrder.DESC
    filtered_users.sort(key=lambda x: x[sort_by], reverse=reverse_order)

    total = len(filtered_users)
    users = filtered_users[skip:skip + limit]

    if include_age:
        users = [user | {"age": user["age"]} for user in users]

    return UsersListResponse(
        users=[UserResponse(**user) for user in users],
        total=total,
        skip=skip,
        limit=limit
    )

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(
    user_id: int = Path(..., gt=0, title="User ID", description="The ID of the user to retrieve.")
):
    """Gets a single user by their ID."""
    user = _find_user_by_id(user_id)
    if not user:
        # If the loop finishes without finding the user, raise a 404 error.
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user_update: UserUpdate):
    """Updates a user's information."""
    user = _find_user_by_id(user_id)
    if not user:
        # If the user doesn't exist, raise a 404 error.
        raise HTTPException(status_code=404, detail="User not found")

    # Get the update data from the request.
    # `exclude_unset=True` means we only get the fields that the client
    # actually sent, allowing for partial updates.
    update_data = user_update.model_dump(exclude_unset=True)

    # Update the user's data field by field.
    for field, value in update_data.items():
        user[field] = value

    return user
