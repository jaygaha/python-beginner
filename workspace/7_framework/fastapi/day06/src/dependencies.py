"""
Dependencies for FastAPI application

How it works:
    *Declare dependencies*
    - Define regular functions, these functions can take parameters, including other dependencies

    *Inject dependencies*
    - Inject dependencies into routes using the `Depends` function (decorated with `@` like @app.get, @app.post)

Benefits:
    - Improved Code Organization: Separates concerns by allowing you to extract shared logic into reusable dependency functions.
    - Enhanced Testability: Dependencies can be easily mocked or replaced during testing.
    - Reusability: Dependencies can be used across multiple routes and endpoints.
    - Reduced duplication of code: Dependencies can be used across multiple routes and endpoints.
    - Better maintainability: Centralizes dependency creation and management, simplifying updates and changes.
    - Automatic Handling: Dependencies can be automatically handled by FastAPI, such as dependency injection and error handling.

"""
from fastapi import Depends, HTTPException, status, Header, Query
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, List
import jwt
from datetime import datetime, timedelta
import hashlib

# Security
security = HTTPBearer()

# Mock user database
users_db = {
    "admin": {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com",
        "hashed_password": hashlib.sha256("admin123".encode()).hexdigest(),
        "roles": ["admin", "user"],
        "is_active": True
    },
    "user": {
        "id": 2,
        "username": "jay",
        "email": "jay@example.com",
        "hashed_password": hashlib.sha256("user123".encode()).hexdigest(),
        "roles": ["user"],
        "is_active": True
    }
}

SECRET_KEY = "python-secret-key" # In real application, this should be a secret key stored securely
ALGORITHM = "HS256"

class User:
    def __init__(self, id: int, username: str, email: str, roles: List[str], is_active: bool):
        self.id = id
        self.username = username
        self.email = email
        self.roles = roles
        self.is_active = is_active

# Database dependency
class DatabaseConnection:
    def __init__(self):
        self.connected = True # Mocked for demonstration purposes, this should be replaced with actual database connection logic
        self.connection_id = f"conn_{datetime.now().timestamp()}"

    def close(self):
        self.connected = False

def get_database():
    db = DatabaseConnection()
    try:
        yield db
    finally:
        db.close()

# Authentication dependencies
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        print(f"Token decoded: username={username}, payload={payload}")  # Debug output
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return username
    except jwt.PyJWTError as e:
        print(f"Token validation failed: {str(e)}")  # Debug output
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

"""
In this get_current_user, verify_token is the dependency that verifies the token and returns the username.
"""
def get_current_user(username: str = Depends(verify_token)) -> User:
    user_data = users_db.get(username)
    if user_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    if not user_data["is_active"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    user_data_without_password = {
        "id": user_data["id"],
        "username": user_data["username"],
        "email": user_data["email"],
        "roles": user_data["roles"],
        "is_active": user_data["is_active"]
    }
    return User(**user_data_without_password)

def get_admin_user(current_user: User = Depends(get_current_user)) -> User:
    if "admin" not in current_user.roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return current_user

# Pagination dependency
class PaginationParams:
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Number of records to skip"),
        limit: int = Query(10, ge=1, le=100, description="Number of records to return")
    ):
        self.skip = skip
        self.limit = limit

# Sorting dependency
class SortingParams:
    def __init__(
        self,
        sort_by: str = Query("id", description="Field to sort by"),
        sort_order: str = Query("asc", patterns="^(asc|desc)$", description="Sort order")
    ):
        self.sort_by = sort_by
        self.sort_order = sort_order

# Rate limiting dependency
class RateLimiter:
    def __init__(self):
        self.requests = {}

    def is_allowed(self, client_ip: str, limit: int = 100, window: int = 3600) -> bool:
        now = datetime.now()
        if client_ip not in self.requests:
            self.requests[client_ip] = []

        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip]
            if (now - req_time).seconds < window
        ]

        if len(self.requests[client_ip]) >= limit:
            return False

        self.requests[client_ip].append(now)
        return True

rate_limiter = RateLimiter()

def check_rate_limit(
    x_forwarded_for: Optional[str] = Header(None),
    x_real_ip: Optional[str] = Header(None)
):
    client_ip = x_forwarded_for or x_real_ip or "127.0.0.1"
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    return client_ip

# Validation dependencies
def validate_positive_int(value: int) -> int:
    if value <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Value must be positive"
        )
    return value

def get_item_id(item_id: int) -> int:
    return validate_positive_int(item_id)

# Common query parameters
class CommonQueryParams:
    def __init__(
        self,
        q: Optional[str] = Query(None, min_length=1, max_length=50, description="Search query"),
        include_inactive: bool = Query(False, description="Include inactive items")
    ):
        self.q = q
        self.include_inactive = include_inactive
