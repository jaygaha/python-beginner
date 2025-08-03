# FastAPI Day 06: Dependencies and Dependency Injection

Welcome to **Day 06** of the FastAPI tutorial! Today you'll learn how to leverage FastAPI's powerful dependency injection system to write cleaner, more modular, and maintainable code.

---

## What You'll Learn

- Understand the core principles of dependency injection in FastAPI.
- Create simple, reusable function-based and class-based dependencies.
- Implement robust authentication and authorization using dependencies.
- Manage complex dependency chains with sub-dependencies.
- Understand and utilize dependency caching for better performance.
- Write effective tests for endpoints that rely on dependencies.

---

## Key Concepts

### 1. Dependency Injection System

**Dependency Injection (DI)** is a design pattern where a component's dependencies (i.e., services or objects it needs to function) are "injected" from an external source rather than created internally. In FastAPI, this is managed by the `Depends` function.

This system allows you to:
-   **Share Logic**: Reuse the same code across multiple endpoints.
-   **Share Database Connections**: Manage the lifecycle of database connections.
-   **Enforce Security**: Implement authentication, authorization, and role-based access control.
-   **Improve Testability**: Easily mock or override dependencies during testing.

### 2. Creating Dependencies

Any function or class that returns a value can be a dependency. You simply define it and then pass it to `Depends` in your path operation function.

**Function-based Dependency:** A simple Python function can serve as a dependency. This is useful for self-contained logic like managing a database session.

Example dependency:
```python
# from dependencies.py

class DatabaseConnection:
    def __init__(self):
        self.connection_id = f"conn_{datetime.now().timestamp()}"

def get_database():
    db = DatabaseConnection()
    try:
        yield db  # Provide the connection
    finally:
        # Code here runs after the request is finished
        print(f"Closing DB connection {db.connection_id}")
```

**Class-based Dependency:** A class can be used to group related request parameters. FastAPI will treat the class itself as a dependency and instantiate it with parameters from the request.

Example dependency for query parameters:
```python
# from dependencies.py

class CommonQueryParams:
    def __init__(
        self,
        q: Optional[str] = Query(None),
        include_inactive: bool = Query(False)
    ):
        self.q = q
        self.include_inactive = include_inactive
```

### 3. Authentication with Dependencies

A common and powerful use case for dependencies is handling security. You can create a dependency that verifies a token and returns the current user.

Example `get_current_user` dependency:
```python
# from dependencies.py

def get_current_user(username: str = Depends(verify_token)) -> User:
    user_data = users_db.get(username)
    if user_data is None or not user_data["is_active"]:
        raise HTTPException(status_code=401, detail="Could not validate credentials")
    return User(**user_data)
```

You can then protect an endpoint by adding this dependency:
```python
# from main.py

@app.get("/users/me")
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user
```
If the token is invalid or the user doesn't exist, the request will be stopped with a `401 Unauthorized` error before your endpoint code is even executed.

### 4. Sub-dependencies and Authorization

Dependencies can depend on other dependencies. FastAPI automatically handles resolving this chain. This is useful for building layers of functionality, like adding authorization on top of authentication.

For example, `get_admin_user` first ensures the user is authenticated by depending on `get_current_user`, and then it performs an additional check to ensure the user has the "admin" role.

Example admin check:
```python
# from dependencies.py

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user
```

### 5. Dependency Caching

Within a single request, FastAPI caches the return value of a dependency. If multiple parts of your code (e.g., your endpoint and another dependency) depend on the same dependency with the same parameters, FastAPI will only call it once and reuse the result.

This is crucial for performance, especially for expensive operations or database connections.

Example of a cached dependency:
```python
# from main.py

# This function will only run once per request, even if multiple
# endpoints or other dependencies require it.
def expensive_operation():
    time.sleep(0.1)  # Simulate delay
    return {"computed_value": "expensive_result"}

@app.get("/expensive")
def get_expensive_data(result=Depends(expensive_operation)):
    return {"expensive_data": result}
```

---

## Next Steps

- Explore `dependencies.py` to see how various dependencies are defined and structured.
- Examine `main.py` and trace how dependencies like `get_current_user` and `get_admin_user` are used to protect different endpoints.
- Run the application and use the interactive API docs at `/api/docs` to test the authenticated endpoints. Try getting a token and using it as a bearer token.
- Review `tests/test_main.py` to understand how to test endpoints that have dependencies.

---

**Tip:** FastAPI’s automatic docs are available at `/api/docs` when you run your app. They will automatically include fields for authentication when you use security dependencies!

---