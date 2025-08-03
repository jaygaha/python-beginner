from fastapi import FastAPI, Depends, HTTPException, status, Form
from dependencies import (
    get_database, get_current_user, get_admin_user, PaginationParams,
    SortingParams, check_rate_limit, get_item_id, CommonQueryParams,
    create_access_token, users_db, User, DatabaseConnection
)
from datetime import timedelta
import hashlib

app = FastAPI(title="Dependency Injection Demo", version="1.0.0")

# Mock data
items_db = [
    {"id": 1, "name": "Item 1", "price": 10.0, "is_active": True, "owner_id": 1},
    {"id": 2, "name": "Item 2", "price": 20.0, "is_active": False, "owner_id": 2},
    {"id": 3, "name": "Item 3", "price": 15.0, "is_active": True, "owner_id": 1},
]

# Authentication endpoints
@app.post("/token")
def login(username: str = Form(), password: str = Form()):
    user_data = users_db.get(username)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if hashed_password != user_data["hashed_password"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "roles": current_user.roles
    }

# Protected endpoints
@app.get("/items/")
def get_items(
    commons: CommonQueryParams = Depends(),
    pagination: PaginationParams = Depends(),
    sorting: SortingParams = Depends(),
    current_user: User = Depends(get_current_user),
    db: DatabaseConnection = Depends(get_database),
    client_ip: str = Depends(check_rate_limit)
):
    # Filter items
    filtered_items = items_db

    if not commons.include_inactive:
        filtered_items = [item for item in filtered_items if item["is_active"]]

    if commons.q:
        filtered_items = [
            item for item in filtered_items
            if commons.q.lower() in item["name"].lower()
        ]

    # Sort items
    reverse_order = sorting.sort_order == "desc"
    if sorting.sort_by in ["id", "name", "price"]:
        filtered_items.sort(key=lambda x: x[sorting.sort_by], reverse=reverse_order)

    # Apply pagination
    total = len(filtered_items)
    items = filtered_items[pagination.skip:pagination.skip + pagination.limit]

    return {
        "items": items,
        "total": total,
        "skip": pagination.skip,
        "limit": pagination.limit,
        "requested_by": current_user.username,
        "client_ip": client_ip,
        "db_connection": db.connection_id
    }

@app.get("/items/{item_id}")
def get_item(
    item_id: int = Depends(get_item_id),
    current_user: User = Depends(get_current_user),
    db: DatabaseConnection = Depends(get_database)
):
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return {
        "item": item,
        "accessed_by": current_user.username,
        "db_connection": db.connection_id
    }

@app.post("/items/")
def create_item(
    item_data: dict,
    current_user: User = Depends(get_current_user),
    db: DatabaseConnection = Depends(get_database)
):
    new_item = {
        "id": len(items_db) + 1,
        "name": item_data["name"],
        "price": item_data["price"],
        "is_active": True,
        "owner_id": current_user.id
    }
    items_db.append(new_item)

    return {
        "item": new_item,
        "created_by": current_user.username,
        "db_connection": db.connection_id
    }

@app.delete("/items/{item_id}")
def delete_item(
    item_id: int = Depends(get_item_id),
    current_user: User = Depends(get_current_user),
    db: DatabaseConnection = Depends(get_database)
):
    item_index = next((i for i, item in enumerate(items_db) if item["id"] == item_id), None)
    if item_index is None:
        raise HTTPException(status_code=404, detail="Item not found")

    item = items_db[item_index]

    # Check ownership or admin rights
    if item["owner_id"] != current_user.id and "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )

    del items_db[item_index]
    return {"message": "Item deleted successfully", "deleted_by": current_user.username}

# Admin-only endpoints
@app.get("/admin/users")
def get_all_users(admin_user: User = Depends(get_admin_user)):
    return {
        "users": list(users_db.values()),
        "accessed_by": admin_user.username
    }

@app.post("/admin/items/{item_id}/activate")
def activate_item(
    item_id: int = Depends(get_item_id),
    admin_user: User = Depends(get_admin_user),
    db: DatabaseConnection = Depends(get_database)
):
    item = next((item for item in items_db if item["id"] == item_id), None)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item["is_active"] = True
    return {
        "message": "Item activated",
        "item": item,
        "activated_by": admin_user.username
    }

# Cached dependency example
def expensive_operation():
    # Simulate expensive operation
    import time
    time.sleep(0.1)  # Simulate delay
    return {"computed_value": "expensive_result", "timestamp": str(datetime.now())}

@app.get("/expensive")
def get_expensive_data(
    result=Depends(expensive_operation),
    current_user: User = Depends(get_current_user)
):
    return {
        "user": current_user.username,
        "expensive_data": result
    }
