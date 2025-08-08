# FastAPI Day 11: Production-Ready Auth with JWT

Welcome to **Day 11** of the FastAPI tutorial series! Today, we're building a production-ready authentication system using JSON Web Tokens (JWT). You'll learn how to structure a FastAPI application with a clean separation of concerns, manage configurations, and implement secure password handling and token-based authentication.

---

## What You'll Learn

-   **Project Structure**: Organize your code into a scalable and maintainable structure with `src`, `core`, `database`, `models`, `routers`, `schemas`, and `services`.
-   **Configuration Management**: Use `pydantic-settings` to manage application settings from environment variables.
-   **Database Integration**: Connect to a database using SQLAlchemy and create tables based on your models.
-   **Password Hashing**: Securely hash and verify passwords with `passlib`.
-   **JWT Authentication**: Implement access and refresh tokens for secure authentication.
-   **Dependency Injection**: Use FastAPI's dependency injection system to manage database sessions and user authentication.
-   **Testing**: Write comprehensive tests for your authentication system using `pytest`.

---

## Key Concepts

For this tutorial, we've structured the application to be more modular and scalable.

-   `src/main.py`: The application's entry point. It initializes the FastAPI app and includes the routers.
-   `src/core/config.py`: Defines the application's configuration using `pydantic-settings`.
-   `src/core/security.py`: Contains all the logic for password hashing and JWT creation and verification.
-   `src/database/connection.py`: Manages the database connection and session.
-   `src/database/crud.py`: Contains functions for creating, reading, and updating data in the database.
-   `src/models/user.py`: Defines the SQLAlchemy user model.
-   `src/routers/auth.py`: Defines the authentication-related endpoints (`/register`, `/login`, `/refresh`).
-   `src/routers/users.py`: Defines user-related endpoints (`/me`).
-   `src/routers/dependencies.py`: Defines dependencies for getting the current authenticated user.
-   `src/schemas/user.py`: Defines the Pydantic models for user-related data.
-   `src/schemas/token.py`: Defines the Pydantic models for token-related data.
-   `src/services/auth_service.py`: Contains the business logic for authentication.
-   `src/services/user_service.py`: Contains the business logic for user-related operations.
-   `tests/`: Contains all the tests for the application.

### 1. Configuration with `pydantic-settings`

We use `pydantic-settings` to manage our application's configuration. This allows us to define our settings in a Pydantic model and automatically load them from environment variables or a `.env` file.

```python-beginner/workspace/7_framework/fastapi/day11/src/core/config.py#L1-L18
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Database
    DATABASE_URL: str = "sqlite:///./app.db"

    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Auth Tutorial"

    class Config:
        env_file = ".env"

settings = Settings()
```

### 2. Password Hashing and JWTs with `passlib` and `python-jose`

We use `passlib` to hash passwords and `python-jose` to create and verify JWTs.

-   **Password Hashing**: We use `passlib`'s `CryptContext` to hash and verify passwords securely.

    ```python-beginner/workspace/7_framework/fastapi/day11/src/core/security.py#L6-L7
    # Password hashing
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    ```

-   **JWT Creation**: We have functions to create both access and refresh tokens, which encapsulate user identity and expiration data.

    ```python-beginner/workspace/7_framework/fastapi/day11/src/core/security.py#L9-L22
    def create_access_token(subject: Union[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        if expires_delta:
            expire = datetime.now() + expires_delta
        else:
            expire = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
        to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    ```

### 3. Dependency Injection for Security

We use FastAPI's powerful dependency injection system to protect endpoints and retrieve the current authenticated user. This keeps the authentication logic clean and reusable.

```python-beginner/workspace/7_framework/fastapi/day11/src/routers/dependencies.py#L8-L34
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not credentials:
        raise credentials_exception

    user_id = verify_token(credentials.credentials)
    if user_id is None:
        raise credentials_exception

    user = get_user_by_id(db, int(user_id))
    if user is None:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )

    return user
```

---

## Next Steps

-   Install the dependencies: `pip install -r requirements.txt`.
-   Create a `.env` file from the `.env.example` and set your `SECRET_KEY`.
-   Run the application with `uvicorn src.main:app --reload`.
-   Use an API client like `curl` or Postman to test the endpoints:
    -   `POST /api/v1/auth/register` to create a new user.
    -   `POST /api/v1/auth/login` to get an access and refresh token.
    -   `GET /api/v1/users/me` with the access token in the `Authorization` header to get your user profile.
    -   `POST /api/v1/auth/refresh` with the refresh token to get a new set of tokens.
-   Run the automated tests with `python -m pytest`.

---