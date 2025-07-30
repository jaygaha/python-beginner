from fastapi import FastAPI, HTTPException
from .models.user import UserCreate, UserResponse, UserUpdate
from datetime import datetime
from typing import List, Dict, Any, Optional

app = FastAPI(title="User Management API", version="1.0.0")

# In-memory database - a simple list to store our user records.
# In a real app, this would be a database like PostgreSQL or MongoDB.
users_db: List[Dict[str, Any]] = []
next_id = 1

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

    # Convert the incoming Pydantic model to a dictionary.
    new_user_data = user.model_dump()

    # IMPORTANT: Never store plain text passwords.
    # We remove it here. In a real app, you would hash the password.
    new_user_data.pop('password')

    # Add server-side generated information.
    new_user_data["id"] = next_id
    new_user_data["created_at"] = datetime.now()
    new_user_data["is_active"] = True

    # Add the new user to our in-memory database.
    users_db.append(new_user_data)
    next_id += 1

    return new_user_data

@app.get("/users", response_model=List[UserResponse])
def get_users():
    """Returns a list of all users in the database."""
    return users_db

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
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
