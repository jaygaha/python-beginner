# Sanic Advanced Tutorial — Day 3

An advanced Sanic web framework tutorial covering query parameters, typed route parameters, JSON validation, async HTTP client requests, and async SQLite database integration.

**Prerequisites:** Complete Day 1 and Day 2 tutorials, understanding of async/await, basic SQL knowledge.

---

## Project Structure

```
day3_sqlite/
├── app/
│   ├── __init__.py          # App initialization with database lifecycle management
│   ├── routes.py            # All route definitions with advanced features
│   ├── database.py          # Async SQLite database connection and operations
│   ├── error_handlers.py    # Enhanced error handling with logging
│   └── config.py            # Configuration management system
├── main.py                  # Application entry point with detailed logging
├── requirements.txt         # Dependencies (sanic, httpx, aiosqlite)
├── README.md               # This file
└── app.db                  # SQLite database file (created automatically)
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

The server will start on `http://localhost:8880` with comprehensive logging enabled.

---

## New Advanced Features

### 1. Query Parameters
Handle URL query parameters with validation and error handling.

### 2. Typed Route Parameters
Use typed URL parameters for automatic type conversion and validation.

### 3. JSON Validation
Robust JSON request body validation with detailed error messages.

### 4. Async HTTP Client
Make external HTTP requests using httpx with proper error handling and timeouts.

### 5. Async SQLite Integration
Complete database integration with aiosqlite for persistent data storage.

### 6. Configuration Management
Centralized configuration system with environment variable support.

### 7. Enhanced Logging
Comprehensive logging throughout the application for debugging and monitoring.

---

## API Endpoints

### 1. Search with Query Parameters
- **URL**: `/api/search?q=<keyword>`
- **Method**: GET
- **Description**: Search functionality demonstrating query parameter handling
- **Query Parameters**: 
  - `q` (required) - Search keyword
- **Response**: `{"result": "You searched for: <keyword>"}`
- **Error**: `{"error": "Missing query parameter 'q'"}` (400) if q is missing

**Examples:**
```bash
# Successful search
curl "http://localhost:8880/api/search?q=python"

# Missing parameter error
curl "http://localhost:8880/api/search"
```

### 2. Typed Route Parameters
- **URL**: `/api/square/<number:int>`
- **Method**: GET
- **Description**: Calculate square of a number using typed route parameters
- **Parameters**: `number` (int) - Integer to square
- **Response**: `{"number": 5, "square": 25}`
- **Error**: 404 if parameter is not an integer

**Examples:**
```bash
# Valid integer
curl http://localhost:8880/api/square/5

# Invalid type (returns 404)
curl http://localhost:8880/api/square/abc
```

### 3. Create Note (JSON Validation)
- **URL**: `/api/notes`
- **Method**: POST
- **Description**: Create a new note with JSON validation
- **Request Body**: `{"content": "Note content"}`
- **Response**: `{"message": "Note added!", "content": "Note content"}`
- **Validation**: Content must be present and non-empty after trimming

**Examples:**
```bash
# Valid note creation
curl -X POST http://localhost:8880/api/notes \
  -H "Content-Type: application/json" \
  -d '{"content": "My first note"}'

# Invalid JSON
curl -X POST http://localhost:8880/api/notes \
  -H "Content-Type: application/json" \
  -d 'invalid json'

# Missing content
curl -X POST http://localhost:8880/api/notes \
  -H "Content-Type: application/json" \
  -d '{}'

# Empty content
curl -X POST http://localhost:8880/api/notes \
  -H "Content-Type: application/json" \
  -d '{"content": "   "}'
```

### 4. Get All Notes
- **URL**: `/api/notes`
- **Method**: GET
- **Description**: Retrieve all notes from the database
- **Response**: `{"notes": [{"id": 1, "content": "Note content"}]}`

**Example:**
```bash
curl http://localhost:8880/api/notes
```

### 5. External IP Service
- **URL**: `/api/external-ip`
- **Method**: GET
- **Description**: Get external IP address using async HTTP client
- **Response**: `{"your_ip": "123.456.789.123"}`
- **Error Handling**: Timeout (504), HTTP errors (502), Service unavailable (503)

**Example:**
```bash
curl http://localhost:8880/api/external-ip
```

---

## Code Features Demonstrated

### 1. Query Parameter Handling
```python
@app.route("/api/search")
async def search(request):
    keyword = request.args.get("q", None)
    if not keyword:
        return json({"error": "Missing query parameter 'q'"}, status=400)
    return json({"result": f"You searched for: {keyword}"})
```

**Features:**
- Access query parameters via `request.args.get()`
- Validation with custom error responses
- Default values and None handling

### 2. Typed Route Parameters
```python
@app.route("/api/square/<number:int>")
async def square(request, number):
    return json({"number": number, "square": number ** 2})
```

**Features:**
- Automatic type conversion from URL string to int
- Built-in validation (non-integers return 404)
- Direct use of typed parameter in handler

### 3. JSON Validation
```python
@app.post("/api/notes")
async def create_note(request):
    try:
        data = await request.json()
    except Exception:
        raise InvalidUsage("Invalid JSON in request body")
    
    if not data or "content" not in data:
        raise InvalidUsage("Missing 'content' in request body")
    
    content = data.get("content", "").strip()
    if not content:
        raise InvalidUsage("Content cannot be empty")
```

**Features:**
- JSON parsing with error handling
- Field presence validation
- Content validation (non-empty after trimming)
- Custom error messages using `InvalidUsage`

### 4. Async HTTP Client
```python
@app.route("/api/external-ip")
async def external_ip(request):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get("https://httpbin.org/ip")
            response.raise_for_status()
            data = response.json()
        return json({"your_ip": data["origin"]})
    except httpx.TimeoutException:
        return json({"error": "Request timeout"}, status=504)
    except httpx.HTTPStatusError as e:
        return json({"error": "External service error"}, status=502)
    except Exception as e:
        return json({"error": "Service unavailable"}, status=503)
```

**Features:**
- Async HTTP requests with httpx
- Timeout configuration
- Comprehensive error handling
- Proper status code mapping

### 5. Async SQLite Integration
```python
class Database:
    def __init__(self):
        self.db = None

    async def connect(self):
        self.db = await aiosqlite.connect('app.db')
        await self.db.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY, content TEXT)')
        await self.db.commit()

    async def add_note(self, content):
        await self.db.execute('INSERT INTO notes (content) VALUES (?)', (content,))
        await self.db.commit()

    async def get_notes(self):
        cursor = await self.db.execute('SELECT id, content FROM notes')
        notes = await cursor.fetchall()
        await cursor.close()
        return [{"id": row[0], "content": row[1]} for row in notes]
```

**Features:**
- Async database operations with aiosqlite
- Connection lifecycle management
- Parameterized queries for security
- Proper cursor handling
- Error handling and logging

### 6. Configuration Management
```python
@dataclass
class AppConfig:
    database: DatabaseConfig
    server: ServerConfig
    http_client: HTTPClientConfig
    logging: LoggingConfig

    @classmethod
    def from_env(cls) -> 'AppConfig':
        return cls(
            database=DatabaseConfig.from_env(),
            server=ServerConfig.from_env(),
            http_client=HTTPClientConfig.from_env(),
            logging=LoggingConfig.from_env()
        )
```

**Features:**
- Dataclass-based configuration
- Environment variable support
- Type hints for better IDE support
- Modular configuration sections

### 7. Enhanced Error Handling
```python
@app.exception(Exception)
async def server_error(request, exception):
    logger.error(f"Server error: {str(exception)} - Path: {request.path}", exc_info=True)
    return json({"error": "Internal server error"}, status=500)
```

**Features:**
- Comprehensive logging with stack traces
- Request path logging for debugging
- Different error types with appropriate responses
- Security (no internal details in production errors)

---

## Database Schema

The application uses a simple SQLite database with the following schema:

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY,
    content TEXT
);
```

**Features:**
- Auto-incrementing primary key
- Simple text content storage
- Created automatically on first run

---

## Configuration Options

The application supports environment-based configuration:

### Database Configuration
- `DATABASE_PATH`: Path to SQLite database file (default: "app.db")
- `DATABASE_TIMEOUT`: Connection timeout in seconds (default: 30.0)

### Server Configuration
- `SERVER_HOST`: Server host address (default: "0.0.0.0")
- `SERVER_PORT`: Server port number (default: 8880)
- `DEBUG`: Enable debug mode (default: "true")
- `ACCESS_LOG`: Enable access logging (default: "true")

### HTTP Client Configuration
- `HTTP_TIMEOUT`: HTTP request timeout in seconds (default: 10.0)
- `HTTP_MAX_RETRIES`: Maximum retry attempts (default: 3)

### Logging Configuration
- `LOG_LEVEL`: Logging level (default: "INFO")
- `LOG_FORMAT`: Log message format (default: timestamp, name, level, message)

**Example Environment Setup:**
```bash
export DATABASE_PATH="/path/to/production.db"
export SERVER_PORT=8000
export DEBUG=false
export LOG_LEVEL=WARNING
python main.py
```

---

## Testing the Application

### 1. Test Query Parameters
```bash
# Valid search
curl "http://localhost:8880/api/search?q=python"

# Test missing parameter
curl "http://localhost:8880/api/search"

# Test with special characters
curl "http://localhost:8880/api/search?q=hello%20world"
```

### 2. Test Typed Parameters
```bash
# Valid integer
curl http://localhost:8880/api/square/42

# Test negative number
curl http://localhost:8880/api/square/-5

# Test invalid type
curl http://localhost:8880/api/square/abc
```

### 3. Test JSON Validation
```bash
# Create valid note
curl -X POST http://localhost:8880/api/notes \
  -H "Content-Type: application/json" \
  -d '{"content": "Test note"}'

# Test invalid JSON
curl -X POST http://localhost:8880/api/notes \
  -H "Content-Type: application/json" \
  -d 'invalid'

# Test missing content
curl -X POST http://localhost:8880/api/notes \
  -H "Content-Type: application/json" \
  -d '{}'
```

### 4. Test Database Operations
```bash
# Create several notes
curl -X POST http://localhost:8880/api/notes \
  -H "Content-Type: application/json" \
  -d '{"content": "First note"}'

curl -X POST http://localhost:8880/api/notes \
  -H "Content-Type: application/json" \
  -d '{"content": "Second note"}'

# Retrieve all notes
curl http://localhost:8880/api/notes
```

### 5. Test External HTTP Client
```bash
# Test successful request
curl http://localhost:8880/api/external-ip

# Test error handling (if httpbin.org is down)
curl http://localhost:8880/api/external-ip
```

---

## Key Learning Objectives

After completing this tutorial, you should understand:

### 1. Advanced Request Handling
- Query parameter validation and processing
- Typed route parameters with automatic conversion
- JSON request body validation and error handling

### 2. Database Integration
- Async SQLite operations with aiosqlite
- Connection lifecycle management
- Parameterized queries for security
- Database schema creation and management

### 3. External Service Integration
- Making async HTTP requests with httpx
- Error handling for network operations
- Timeout configuration and retry logic
- Status code mapping and error responses

### 4. Configuration Management
- Environment-based configuration
- Type-safe configuration with dataclasses
- Modular configuration organization

### 5. Production Considerations
- Comprehensive logging and monitoring
- Error handling and user-friendly error messages
- Security best practices (parameterized queries, no internal error exposure)
- Resource management and cleanup

---

## Performance Considerations

### Database Performance
- **Connection Pooling**: Single connection for simplicity (consider connection pooling for production)
- **Query Optimization**: Use indexes for frequently queried fields
- **Batch Operations**: Consider bulk inserts for high-throughput scenarios

### HTTP Client Performance
- **Connection Reuse**: httpx automatically handles connection pooling
- **Timeout Configuration**: Appropriate timeouts prevent hanging requests
- **Error Handling**: Graceful degradation when external services fail

### Memory Management
- **Cursor Cleanup**: Proper cursor closing prevents memory leaks
- **Connection Management**: Lifecycle listeners ensure proper cleanup
- **Logging**: Structured logging for better performance monitoring

---

## Error Handling Patterns

### 1. Validation Errors (400)
```python
if not keyword:
    return json({"error": "Missing query parameter 'q'"}, status=400)
```

### 2. Client Errors (4xx)
```python
# Automatic 404 for invalid typed parameters
@app.route("/api/square/<number:int>")
```

### 3. Server Errors (5xx)
```python
except Exception as e:
    logger.error(f"Unexpected error: {e}")
    return json({"error": "Service unavailable"}, status=503)
```

### 4. External Service Errors
```python
except httpx.TimeoutException:
    return json({"error": "Request timeout"}, status=504)
except httpx.HTTPStatusError:
    return json({"error": "External service error"}, status=502)
```

---

## Best Practices Demonstrated

### 1. Input Validation
- Always validate query parameters
- Check JSON structure before processing
- Sanitize input data (strip whitespace)
- Provide meaningful error messages

### 2. Database Operations
- Use parameterized queries
- Handle connection errors gracefully
- Implement proper resource cleanup
- Log database operations for debugging

### 3. HTTP Client Usage
- Set appropriate timeouts
- Handle different types of HTTP errors
- Use context managers for resource management
- Implement retry logic where appropriate

### 4. Configuration Management
- Use environment variables for configuration
- Provide sensible defaults
- Organize configuration logically
- Support type conversion

### 5. Logging and Monitoring
- Log important events and errors
- Include context information (request path, user input)
- Use appropriate log levels
- Structure logs for easy parsing

---

## Next Steps

After mastering this tutorial, consider exploring:

### 1. Advanced Database Features
- Connection pooling with asyncpg or similar
- Database migrations
- ORM integration (SQLAlchemy with async support)
- Database transactions and rollbacks

### 2. Authentication and Authorization
- JWT token authentication
- Session management
- Role-based access control
- API key authentication

### 3. Testing
- Unit tests for database operations
- Integration tests for API endpoints
- Mock external service calls
- Performance testing

### 4. Production Deployment
- Docker containerization
- Environment-specific configuration
- Health checks and monitoring
- Load balancing and scaling

### 5. Advanced Features
- WebSocket support for real-time features
- Background task processing
- Caching strategies
- Rate limiting and throttling

---

## Troubleshooting

### Common Issues

#### Database Connection Problems
```python
# Check if database file is writable
# Verify aiosqlite installation
# Check database path configuration
```

#### JSON Parsing Errors
```python
# Verify Content-Type header
# Check JSON syntax
# Validate request body size
```

#### HTTP Client Timeouts
```python
# Check network connectivity
# Verify external service availability
# Adjust timeout configuration
```

#### Configuration Issues
```python
# Check environment variable names
# Verify type conversions
# Validate configuration values
```

### Debugging Tips

1. **Enable Debug Mode**: Set `DEBUG=true` for detailed error messages
2. **Check Logs**: Monitor console output for error messages and warnings
3. **Test Endpoints**: Use curl or Postman to test individual endpoints
4. **Database Inspection**: Use SQLite browser to inspect database contents
5. **Network Testing**: Test external services independently

---

## Conclusion

This tutorial demonstrates advanced Sanic features including database integration, external service calls, and robust error handling. The combination of async operations, proper configuration management, and comprehensive logging creates a foundation for production-ready applications.

The skills learned here are directly applicable to building scalable web APIs, microservices, and data-driven applications with Sanic.

Happy coding with Sanic!