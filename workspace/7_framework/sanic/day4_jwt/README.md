# Sanic JWT Authentication Tutorial — Day 4

An advanced Sanic web framework tutorial covering JWT authentication, request validation with sanic-ext, middleware-based route protection, and secure API development.

**Prerequisites:** Complete Day 1, Day 2, and Day 3 tutorials, understanding of authentication concepts, JWT tokens, and API security.

---

## Project Structure

```
day4_jwt/
├── app/
│   ├── __init__.py          # App initialization with sanic-ext and middleware
│   ├── routes.py            # Authentication and protected routes
│   ├── auth.py              # JWT token creation, validation, and middleware
│   ├── error_handlers.py    # Enhanced error handling for auth errors
│   └── schema.py            # Request validation schemas using dataclasses
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies (sanic, sanic-ext, pyjwt)
└── README.md               # This file
```

## Setup Instructions

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Run the application:

```bash
python main.py
```

The server will start on `http://localhost:8880` with JWT authentication enabled.

---

## New Advanced Features

### 1. JWT Authentication
Complete JWT (JSON Web Token) implementation for stateless authentication with token creation, validation, and middleware protection.

### 2. Sanic-ext Integration
Leverage sanic-ext for advanced features including request validation, dependency injection, and enhanced functionality.

### 3. Request Validation
Robust request validation using dataclasses with automatic error handling and type checking.

### 4. Authentication Middleware
Middleware-based route protection that automatically validates JWT tokens for protected endpoints.

### 5. Security Best Practices
Implementation of secure authentication patterns including proper token handling and error responses.

---

## Authentication Flow

### 1. User Login
1. Client sends credentials to `/api/login`
2. Server validates credentials against user store
3. Server creates JWT token with user information
4. Client receives token for subsequent requests

### 2. Protected Route Access
1. Client includes JWT token in Authorization header
2. Middleware validates token automatically
3. User information is attached to request context
4. Route handler accesses authenticated user data

### 3. Token Validation
- Tokens are validated on every protected route request
- Expired or invalid tokens return 401 Unauthorized
- Valid tokens provide access to protected resources

---

## API Endpoints

### Authentication Endpoints

#### 1. User Login
- **URL**: `/api/login`
- **Method**: POST
- **Description**: Authenticate user and receive JWT token
- **Request Body**: `{"username": "jay", "password": "secret"}`
- **Response**: `{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}`
- **Validation**: Username and password are required fields

**Example:**
```bash
curl -X POST http://localhost:8880/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "jay", "password": "secret"}'
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.example_token_signature"
}
```

### Protected Endpoints (Require Authentication)

#### 2. Create Note
- **URL**: `/api/secure/notes`
- **Method**: POST
- **Description**: Create a new note for authenticated user
- **Headers**: `Authorization: Bearer <jwt_token>`
- **Request Body**: `{"title": "Note Title", "content": "Note content"}`
- **Response**: `{"message": "Note added!"}`
- **Validation**: Title and content are required fields

**Example:**
```bash
curl -X POST http://localhost:8880/api/secure/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{"title": "My Note", "content": "This is my note content"}'
```

#### 3. List User Notes
- **URL**: `/api/secure/notes`
- **Method**: GET
- **Description**: Get all notes for authenticated user
- **Headers**: `Authorization: Bearer <jwt_token>`
- **Response**: `{"notes": [{"user": 1, "content": "Note content"}]}`

**Example:**
```bash
curl http://localhost:8880/api/secure/notes \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

---

## Code Features Demonstrated

### 1. JWT Token Creation
```python
def create_token(user_id: int) -> str:
    payload = {"user_id": user_id}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
```

**Features:**
- Secure token creation with user information
- Configurable secret key and algorithm
- Compact, URL-safe token format
- Stateless authentication (no server-side session storage)

### 2. JWT Token Validation
```python
def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise Unauthorized("Token has expired")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid token")
    except jwt.PyJWTError:
        raise Unauthorized("Invalid or expired token")
```

**Features:**
- Comprehensive error handling for different token issues
- Automatic token expiration checking
- Secure token verification with secret key
- Custom error messages for different scenarios

### 3. Authentication Middleware
```python
async def auth_middleware(request: Request):
    if request.path.startswith("/api/secure"):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise Unauthorized("Missing Bearer token")

        token = auth_header.split()[1]
        payload = decode_token(token)
        request.ctx.user = payload.get("user_id")
```

**Features:**
- Automatic protection for `/api/secure` routes
- Bearer token extraction from Authorization header
- User information attached to request context
- Centralized authentication logic

### 4. Request Validation with Sanic-ext
```python
@dataclass
class LoginRequest:
    username: str
    password: str

@app.post("/api/login")
@validate(json=LoginRequest)
async def login(request: Request, body: LoginRequest):
    # body is automatically validated and typed
    user = users.get(body.username)
    if not user or user["password"] != body.password:
        return json({"error": "Invalid credentials"}, status=401)
```

**Features:**
- Automatic JSON validation using dataclasses
- Type checking and conversion
- Descriptive error messages for invalid requests
- Clean, typed access to request data

### 5. Protected Route Implementation
```python
@app.post("/api/secure/notes")
@validate(json=NoteCreateRequest)
async def create_note(request: Request, body: NoteCreateRequest):
    # request.ctx.user is automatically populated by middleware
    notes.append({"user": request.ctx.user, "content": body.content})
    return json({"message": "Note added!"})
```

**Features:**
- Automatic authentication via middleware
- Access to authenticated user information
- Request validation with custom schemas
- User-specific data operations

---

## Security Considerations

### 1. JWT Secret Key
```python
# In production, use environment variables
JWT_SECRET = os.getenv("JWT_SECRET", "your_secret_key_123")
```

**Important:**
- Never hardcode secrets in production
- Use strong, random secret keys
- Rotate secrets regularly
- Store secrets securely (environment variables, key management systems)

### 2. Token Expiration
```python
# Add expiration to tokens
payload = {
    "user_id": user_id,
    "exp": datetime.utcnow() + timedelta(hours=1)
}
```

**Best Practices:**
- Set appropriate expiration times
- Implement token refresh mechanisms
- Handle expired tokens gracefully
- Consider different expiration times for different token types

### 3. HTTPS in Production
```python
# Force HTTPS in production
app.config.FORCE_HTTPS = True
```

**Security Requirements:**
- Always use HTTPS in production
- Secure cookie settings
- Proper CORS configuration
- Input validation and sanitization

### 4. Error Handling
```python
@app.exception(Unauthorized)
async def handle_auth_error(request, exception):
    return json({"error": str(exception)}, status=401)
```

**Security Principles:**
- Don't expose internal system details
- Use consistent error responses
- Log security events for monitoring
- Implement rate limiting for authentication endpoints

---

## Testing the Application

### 1. Test User Login
```bash
# Valid credentials
curl -X POST http://localhost:8880/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "jay", "password": "secret"}'

# Invalid credentials
curl -X POST http://localhost:8880/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "jay", "password": "wrong"}'

# Missing fields
curl -X POST http://localhost:8880/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "jay"}'
```

### 2. Test Protected Routes
```bash
# First, get a token
TOKEN=$(curl -X POST http://localhost:8880/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "jay", "password": "secret"}' \
  | jq -r '.token')

# Create a note with valid token
curl -X POST http://localhost:8880/api/secure/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "Test Note", "content": "This is a test note"}'

# List notes with valid token
curl http://localhost:8880/api/secure/notes \
  -H "Authorization: Bearer $TOKEN"

# Try without token (should fail)
curl http://localhost:8880/api/secure/notes

# Try with invalid token (should fail)
curl http://localhost:8880/api/secure/notes \
  -H "Authorization: Bearer invalid_token"
```

### 3. Test Request Validation
```bash
# Test missing required fields
curl -X POST http://localhost:8880/api/secure/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"title": "Test Note"}'

# Test invalid JSON
curl -X POST http://localhost:8880/api/secure/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d 'invalid json'
```

---

## Key Learning Objectives

After completing this tutorial, you should understand:

### 1. JWT Authentication
- How JWT tokens work and their structure
- Token creation and validation processes
- Stateless authentication benefits and challenges
- Security considerations for JWT implementation

### 2. Sanic-ext Integration
- Advanced Sanic features through extensions
- Request validation with dataclasses
- Automatic error handling and type conversion
- Enhanced development experience

### 3. Middleware-based Security
- Authentication middleware patterns
- Request context manipulation
- Route protection strategies
- Centralized security logic

### 4. Request Validation
- Schema-based validation with dataclasses
- Automatic error responses for invalid data
- Type safety and IDE support
- Clean separation of validation logic

### 5. Secure API Development
- Authentication vs. authorization
- Token-based security patterns
- Error handling for security scenarios
- Production security considerations

---

## Expanding the Application

### 1. Add User Registration
```python
@app.post("/api/register")
@validate(json=UserRegistrationRequest)
async def register(request: Request, body: UserRegistrationRequest):
    # Hash password, create user, return token
    pass
```

### 2. Implement Token Refresh
```python
@app.post("/api/refresh")
async def refresh_token(request: Request):
    # Validate refresh token, issue new access token
    pass
```

### 3. Add Role-based Authorization
```python
def require_role(role: str):
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            if request.ctx.user.role != role:
                raise Unauthorized("Insufficient permissions")
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
```

### 4. Database Integration
```python
# Replace in-memory storage with database
async def authenticate_user(username: str, password: str) -> Optional[User]:
    # Query database, verify password hash
    pass
```

---

## Production Considerations

### 1. Environment Configuration
```python
# config.py
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", "1"))
```

### 2. Password Security
```python
import bcrypt

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

### 3. Rate Limiting
```python
from sanic_ext import limiter

@app.post("/api/login")
@limiter.limit("5 per minute")
async def login(request: Request):
    # Limit login attempts
    pass
```

### 4. Logging and Monitoring
```python
import logging

logger = logging.getLogger(__name__)

@app.post("/api/login")
async def login(request: Request):
    logger.info(f"Login attempt for user: {body.username}")
    # Log security events
```

---

## Testing Strategy

### 1. Unit Tests
```python
import pytest
from app.auth import create_token, decode_token

def test_token_creation():
    token = create_token(123)
    payload = decode_token(token)
    assert payload["user_id"] == 123

def test_invalid_token():
    with pytest.raises(Unauthorized):
        decode_token("invalid_token")
```

### 2. Integration Tests
```python
async def test_protected_route_without_token(app):
    request, response = await app.asgi_client.get("/api/secure/notes")
    assert response.status == 401

async def test_protected_route_with_token(app):
    # Login and get token
    login_response = await app.asgi_client.post("/api/login", json={
        "username": "jay",
        "password": "secret"
    })
    token = login_response.json["token"]
    
    # Access protected route
    request, response = await app.asgi_client.get(
        "/api/secure/notes",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status == 200
```

---

## Common Issues and Solutions

### 1. Token Expiration
**Problem:** Tokens expire and users get 401 errors
**Solution:** Implement token refresh or increase expiration time

### 2. Missing Authorization Header
**Problem:** Requests fail with "Missing Bearer token"
**Solution:** Ensure all protected requests include Authorization header

### 3. Invalid Token Format
**Problem:** Tokens are malformed or corrupted
**Solution:** Validate token format and handle parsing errors

### 4. Middleware Order
**Problem:** Authentication middleware runs after route handlers
**Solution:** Ensure middleware is registered before routes

---

## Best Practices

### 1. Security
- Use strong secret keys
- Implement token expiration
- Validate all inputs
- Use HTTPS in production
- Log security events

### 2. Error Handling
- Provide meaningful error messages
- Use appropriate HTTP status codes
- Don't expose internal details
- Handle edge cases gracefully

### 3. Code Organization
- Separate authentication logic
- Use validation schemas
- Implement proper error handling
- Keep routes clean and focused

### 4. Testing
- Test authentication flows
- Validate security scenarios
- Test error conditions
- Use integration tests

---

## Next Steps

After mastering this tutorial, consider exploring:

### 1. Advanced Authentication
- OAuth2 integration
- Multi-factor authentication
- Social login providers
- Single sign-on (SSO)

### 2. Authorization Patterns
- Role-based access control (RBAC)
- Attribute-based access control (ABAC)
- Permission systems
- Resource-based authorization

### 3. Security Enhancements
- Rate limiting and throttling
- API key management
- Request signing
- Security headers

### 4. Production Features
- Token blacklisting
- Session management
- Audit logging
- Security monitoring

---

## Conclusion

This tutorial demonstrates comprehensive JWT authentication implementation with Sanic, including request validation, middleware-based protection, and security best practices. The combination of JWT tokens, sanic-ext validation, and proper error handling creates a robust foundation for secure API development.

The authentication patterns learned here are essential for building production-ready APIs that require user authentication and authorization.

Happy coding with secure Sanic applications!