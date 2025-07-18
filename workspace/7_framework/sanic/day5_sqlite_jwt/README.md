# Sanic Production-Ready Tutorial — Day 5

A comprehensive Sanic web framework tutorial combining all advanced features: JWT authentication, SQLite database, file uploads/downloads, pagination, CORS support, and production-ready security patterns.

**Prerequisites:** Complete Day 1-4 tutorials, understanding of authentication, databases, file handling, and security best practices.

**Previous Tutorial:** [Day 4 - JWT Authentication](../day4_jwt/README.md)

---

## Project Structure

```
day5_sqlite_jwt/
├── app/
│   ├── __init__.py          # App initialization with CORS, database lifecycle
│   ├── routes.py            # Complete API routes with security and validation
│   ├── auth.py              # JWT authentication with bcrypt password hashing
│   ├── db.py                # SQLite database connection management
│   └── models.py            # Database operations for users and notes
├── uploads/                 # Secure file upload directory
│   └── .gitignore          # Git ignore for uploaded files
├── main.py                  # Application entry point
├── requirements.txt         # All dependencies
├── README.md               # This file
└── app.db                  # SQLite database (created automatically)
```

## Setup Instructions

### Install dependencies:

```bash
pip install -r requirements.txt
```

### Environment Variables (Optional):

```bash
export JWT_SECRET="your-production-secret-key-here"
export DEBUG=false
export LOG_LEVEL=INFO
```

### Run the application:

```bash
python main.py
```

The server will start on `http://localhost:8880` with full production features enabled.

---

## Advanced Features Combined

### 1. **Secure Authentication System**
- JWT token-based authentication with configurable secrets
- bcrypt password hashing for secure storage
- Input validation for registration and login
- Middleware-based route protection

### 2. **Database Integration**
- Async SQLite operations with aiosqlite
- User management with secure password storage
- Notes system with user-specific access
- Comprehensive error handling and logging

### 3. **File Upload/Download System**
- Secure file upload with validation
- File type and size restrictions
- Path traversal protection
- Unique filename generation

### 4. **Pagination & Query Parameters**
- Configurable pagination for notes
- Input validation for pagination parameters
- Efficient database queries with LIMIT/OFFSET

### 5. **CORS Support**
- Full CORS configuration for frontend integration
- Configurable origins and methods
- Support for preflight requests

### 6. **Production Security**
- Comprehensive input validation
- SQL injection prevention
- File upload security
- Request/response logging

---

## Complete API Documentation

### Authentication Endpoints

#### 1. User Registration
- **URL**: `/api/register`
- **Method**: POST
- **Description**: Register a new user with secure password hashing
- **Request Body**: 
  ```json
  {
    "username": "john_doe",
    "password": "securepassword123"
  }
  ```
- **Response**: `{"message": "User registered"}`
- **Validation**: 
  - Username: 3-50 characters, alphanumeric with hyphens/underscores
  - Password: minimum 6 characters
- **Errors**: 
  - 400: Invalid input or missing fields
  - 409: Username already taken

**Example:**
```bash
curl -X POST http://localhost:8880/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "securepassword123"}'
```

#### 2. User Login
- **URL**: `/api/login`
- **Method**: POST
- **Description**: Authenticate user and receive JWT token
- **Request Body**: 
  ```json
  {
    "username": "john_doe",
    "password": "securepassword123"
  }
  ```
- **Response**: `{"token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."}`
- **Errors**: 
  - 400: Missing username or password
  - 401: Invalid credentials

**Example:**
```bash
curl -X POST http://localhost:8880/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "john_doe", "password": "securepassword123"}'
```

### Protected Endpoints (Require JWT Token)

#### 3. Create Note
- **URL**: `/api/secure/notes`
- **Method**: POST
- **Description**: Create a new note for authenticated user
- **Headers**: `Authorization: Bearer <jwt_token>`
- **Request Body**: 
  ```json
  {
    "content": "This is my note content"
  }
  ```
- **Response**: `{"message": "Note added"}`
- **Validation**: 
  - Content: required, non-empty, max 1000 characters
- **Errors**: 
  - 400: Invalid content or missing fields
  - 401: Missing or invalid token
  - 500: Database error

**Example:**
```bash
TOKEN="your_jwt_token_here"
curl -X POST http://localhost:8880/api/secure/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content": "My first secure note"}'
```

#### 4. List Notes with Pagination
- **URL**: `/api/secure/notes`
- **Method**: GET
- **Description**: Get paginated list of user's notes
- **Headers**: `Authorization: Bearer <jwt_token>`
- **Query Parameters**:
  - `limit` (optional): Number of notes per page (1-100, default: 5)
  - `offset` (optional): Number of notes to skip (default: 0)
- **Response**: 
  ```json
  {
    "notes": [
      {"id": 1, "content": "First note"},
      {"id": 2, "content": "Second note"}
    ]
  }
  ```
- **Errors**: 
  - 400: Invalid pagination parameters
  - 401: Missing or invalid token
  - 500: Database error

**Examples:**
```bash
# Get first 5 notes
curl http://localhost:8880/api/secure/notes \
  -H "Authorization: Bearer $TOKEN"

# Get next 10 notes
curl "http://localhost:8880/api/secure/notes?limit=10&offset=5" \
  -H "Authorization: Bearer $TOKEN"
```

#### 5. File Upload
- **URL**: `/api/secure/upload`
- **Method**: POST
- **Description**: Upload a file with security validation
- **Headers**: `Authorization: Bearer <jwt_token>`
- **Request Body**: Multipart form data with file field
- **Response**: 
  ```json
  {
    "message": "File uploaded",
    "filename": "abc123def456.pdf",
    "original_name": "document.pdf"
  }
  ```
- **Security Features**:
  - File type validation (txt, pdf, png, jpg, jpeg, gif, doc, docx)
  - File size limit (10MB)
  - Secure filename generation
  - Path traversal protection
- **Errors**: 
  - 400: No file, invalid type, or missing token
  - 413: File too large
  - 500: Upload failed

**Example:**
```bash
curl -X POST http://localhost:8880/api/secure/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@/path/to/your/document.pdf"
```

#### 6. File Download
- **URL**: `/api/secure/download/<filename>`
- **Method**: GET
- **Description**: Download a previously uploaded file
- **Headers**: `Authorization: Bearer <jwt_token>`
- **Parameters**: `filename` - The secure filename returned from upload
- **Response**: File content with appropriate headers
- **Security Features**:
  - Path traversal protection
  - Filename validation
  - Access to upload directory only
- **Errors**: 
  - 400: Invalid filename
  - 401: Missing or invalid token
  - 404: File not found

**Example:**
```bash
curl http://localhost:8880/api/secure/download/abc123def456.pdf \
  -H "Authorization: Bearer $TOKEN" \
  -o downloaded_file.pdf
```

---

## Security Features Implementation

### 1. **Password Security**
```python
def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
```

**Features:**
- bcrypt hashing with automatic salt generation
- Secure password comparison
- Protection against timing attacks

### 2. **JWT Token Security**
```python
JWT_SECRET = os.getenv("JWT_SECRET", "supersecret")
JWT_ALGORITHM = "HS256"

def create_token(user_id):
    return jwt.encode({"user_id": user_id}, JWT_SECRET, algorithm=JWT_ALGORITHM)
```

**Features:**
- Configurable secret key via environment variables
- Secure token generation and validation
- Automatic token verification in middleware

### 3. **File Upload Security**
```python
def secure_filename(filename):
    """Generate a secure filename to prevent path traversal"""
    if not filename:
        return None
    ext = Path(filename).suffix.lower()
    return f"{uuid.uuid4().hex}{ext}"
```

**Features:**
- UUID-based filename generation
- File extension validation
- Path traversal prevention
- File size limits

### 4. **Input Validation**
```python
def validate_user_input(username, password):
    """Validate username and password input"""
    if not username or not password:
        return False, "Username and password are required"
    if len(username) < 3 or len(username) > 50:
        return False, "Username must be between 3 and 50 characters"
    # ... more validation
```

**Features:**
- Comprehensive input validation
- Length and format checking
- SQL injection prevention
- XSS protection

---

## Database Schema

The application uses SQLite with the following tables:

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);
```

### Notes Table
```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    content TEXT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

**Features:**
- Auto-incrementing primary keys
- Foreign key relationships
- Unique constraints
- Proper indexing for performance

---

## Configuration & Environment

### Environment Variables
```bash
# Security
export JWT_SECRET="your-production-secret-key-here"

# Database
export DATABASE_PATH="/path/to/production.db"

# Server
export SERVER_HOST="0.0.0.0"
export SERVER_PORT=8880
export DEBUG=false

# Logging
export LOG_LEVEL=INFO
```

### CORS Configuration
```python
CORS(app, resources=r'/api/*', origins="*", methods=["GET", "POST", "HEAD", "OPTIONS"])
```

**Features:**
- Configurable origins and methods
- Support for preflight requests
- API endpoint protection
- Frontend integration ready

---

## Testing the Complete Application

### 1. **Test User Registration and Login**
```bash
# Register a new user
curl -X POST http://localhost:8880/api/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# Login and get token
TOKEN=$(curl -X POST http://localhost:8880/api/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}' \
  | jq -r '.token')

echo "Token: $TOKEN"
```

### 2. **Test Notes System**
```bash
# Create some notes
curl -X POST http://localhost:8880/api/secure/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content": "First note"}'

curl -X POST http://localhost:8880/api/secure/notes \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"content": "Second note"}'

# List notes with pagination
curl "http://localhost:8880/api/secure/notes?limit=10&offset=0" \
  -H "Authorization: Bearer $TOKEN"
```

### 3. **Test File Upload/Download**
```bash
# Upload a file
echo "Test file content" > test.txt
UPLOAD_RESPONSE=$(curl -X POST http://localhost:8880/api/secure/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.txt")

echo "Upload response: $UPLOAD_RESPONSE"

# Extract filename from response
FILENAME=$(echo $UPLOAD_RESPONSE | jq -r '.filename')

# Download the file
curl http://localhost:8880/api/secure/download/$FILENAME \
  -H "Authorization: Bearer $TOKEN" \
  -o downloaded_test.txt

# Verify file content
cat downloaded_test.txt
```

### 4. **Test Security Features**
```bash
# Test without token (should fail)
curl http://localhost:8880/api/secure/notes

# Test with invalid token (should fail)
curl http://localhost:8880/api/secure/notes \
  -H "Authorization: Bearer invalid_token"

# Test invalid file upload (should fail)
curl -X POST http://localhost:8880/api/secure/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@malicious.exe"
```

---

## Performance Considerations

### 1. **Database Optimization**
- Connection pooling for production
- Proper indexing on frequently queried columns
- Parameterized queries to prevent SQL injection
- Efficient pagination with LIMIT/OFFSET

### 2. **File Upload Performance**
- Streaming file uploads for large files
- File size validation before processing
- Efficient file storage with UUID naming
- Cleanup of temporary files

### 3. **Authentication Performance**
- JWT tokens reduce database lookups
- bcrypt work factor tuning for security/performance balance
- Token caching strategies
- Session management optimization

### 4. **Memory Management**
- Proper database connection cleanup
- File handle management
- Request/response streaming
- Resource cleanup in listeners

---

## Production Deployment

### 1. **Security Checklist**
- [ ] Set strong JWT secret in environment variables
- [ ] Use HTTPS in production
- [ ] Configure proper CORS origins
- [ ] Set up rate limiting
- [ ] Enable request/response logging
- [ ] Configure file upload limits
- [ ] Set up database backups

### 2. **Configuration**
```python
# Production settings
app.config.DEBUG = False
app.config.ACCESS_LOG = True
app.config.KEEP_ALIVE = True
app.config.KEEP_ALIVE_TIMEOUT = 30
```

### 3. **Deployment Options**
- **Docker**: Containerized deployment
- **Gunicorn**: WSGI server with multiple workers
- **Nginx**: Reverse proxy for static files
- **Supervisor**: Process management
- **Systemd**: Service management

### 4. **Monitoring**
- Application logs with structured logging
- Database performance monitoring
- File upload/download metrics
- Authentication success/failure rates
- Error tracking and alerting

---

## Error Handling Patterns

### 1. **Authentication Errors**
```python
# 401 Unauthorized
{"error": "Missing Bearer token"}
{"error": "Invalid token"}
{"error": "Invalid credentials"}
```

### 2. **Validation Errors**
```python
# 400 Bad Request
{"error": "Username must be between 3 and 50 characters"}
{"error": "Content cannot be empty"}
{"error": "Invalid pagination parameters"}
```

### 3. **File Upload Errors**
```python
# 400 Bad Request
{"error": "No file uploaded"}
{"error": "File type not allowed"}

# 413 Payload Too Large
{"error": "File too large"}
```

### 4. **Database Errors**
```python
# 500 Internal Server Error
{"error": "Failed to add note"}
{"error": "Failed to fetch notes"}

# 409 Conflict
{"error": "Username already taken"}
```

---

## Best Practices Demonstrated

### 1. **Security**
- Never store plain text passwords
- Use environment variables for secrets
- Validate all user inputs
- Implement proper error handling
- Use HTTPS in production

### 2. **Database**
- Use parameterized queries
- Implement proper connection management
- Handle database errors gracefully
- Log database operations
- Use transactions where appropriate

### 3. **File Handling**
- Validate file types and sizes
- Generate secure filenames
- Prevent path traversal attacks
- Clean up temporary files
- Implement proper access controls

### 4. **API Design**
- Use appropriate HTTP status codes
- Implement pagination for large datasets
- Provide meaningful error messages
- Use consistent response formats
- Document all endpoints

---

## Advanced Features to Explore

### 1. **Enhanced Authentication**
- Token refresh mechanisms
- Multi-factor authentication
- OAuth2 integration
- Session management

### 2. **Database Enhancements**
- Connection pooling
- Database migrations
- ORM integration
- Caching strategies

### 3. **File Management**
- Cloud storage integration
- Image processing
- File versioning
- Metadata extraction

### 4. **Performance Optimization**
- Redis caching
- Background task processing
- Load balancing
- CDN integration

---

## Troubleshooting Guide

### Common Issues

#### 1. **Database Connection Errors**
```bash
# Check database file permissions
ls -la app.db

# Verify aiosqlite installation
pip show aiosqlite
```

#### 2. **JWT Token Issues**
```bash
# Check token format
echo "TOKEN" | base64 -d

# Verify secret configuration
echo $JWT_SECRET
```

#### 3. **File Upload Problems**
```bash
# Check upload directory permissions
ls -la uploads/

# Verify file size limits
du -h uploads/
```

#### 4. **CORS Issues**
```bash
# Test preflight request
curl -X OPTIONS http://localhost:8880/api/login \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST"
```

---

## Conclusion

This Day 5 tutorial represents a complete, production-ready Sanic application that combines all the advanced features learned in previous tutorials:

- **Secure Authentication**: JWT tokens with bcrypt password hashing
- **Database Integration**: Async SQLite with proper error handling
- **File Management**: Secure upload/download with validation
- **API Security**: Comprehensive input validation and protection
- **Frontend Integration**: Full CORS support for modern web apps

The application demonstrates real-world patterns and best practices that can be directly applied to production systems. It provides a solid foundation for building scalable, secure web APIs with Sanic.

### Key Achievements:
- ✅ Complete user authentication system
- ✅ Secure file upload/download functionality
- ✅ Database-backed note management
- ✅ Pagination and query parameter handling
- ✅ Comprehensive security measures
- ✅ Production-ready configuration
- ✅ Full CORS support for frontend integration

This tutorial completes the Sanic learning journey from basic concepts to advanced, production-ready applications.

Happy coding with Sanic!