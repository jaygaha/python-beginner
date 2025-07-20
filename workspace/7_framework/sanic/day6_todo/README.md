# Sanic Todo API Tutorial — Day 6

A comprehensive Sanic web framework tutorial demonstrating a complete Todo API implementation with dependency injection, service architecture, input validation, error handling, and comprehensive testing. This tutorial showcases best practices for building maintainable and robust APIs.

**Prerequisites:** Complete Day 1-5 tutorials, understanding of service-oriented architecture, dependency injection patterns, and API design principles.

**Previous Tutorial:** [Day 5 - Production-Ready Application](../day5_sqlite_jwt/README.md)

---

## Project Structure

```
day6_todo/
├── app/
│   ├── __init__.py          # App initialization with dependency injection
│   ├── routes.py            # Complete Todo API routes with validation
│   ├── services.py          # Business logic with UserService and TodoService
│   └── types.py             # TypedDict models for data structures
├── main.py                  # Application entry point
├── requirements.txt         # Dependencies (sanic, sanic-ext)
├── test_app.py             # Comprehensive API testing suite
├── test_server.py          # Server startup and health check tests
└── README.md               # This file
```

## What's New in Day 6

### 1. **Service-Oriented Architecture**
- Clean separation of concerns with dedicated service classes
- Dependency injection using sanic-ext for loose coupling
- Business logic encapsulation away from route handlers

### 2. **Comprehensive Todo Management**
- Full CRUD operations for todos and users
- User-specific todo filtering and management
- Advanced todo operations (toggle completion, updates)

### 3. **Production-Quality Validation**
- Robust input validation with detailed error messages
- Type safety with proper error handling
- Comprehensive request/response validation

### 4. **Testing Infrastructure**
- Complete test suites for all API endpoints
- Server health check and startup verification
- Error scenario testing and validation

### 5. **Bug Fixes and Best Practices**
- Documented common issues and their solutions
- Type conversion and validation patterns
- Proper error handling and user feedback

---

## Key Features Demonstrated

### 1. **Dependency Injection with Sanic-ext**
```python
# In app/__init__.py
ext = Extend(app)
ext.add_dependency(UserService)
ext.add_dependency(TodoService)

# In routes
async def list_users(request: Request, user_service: UserService) -> HTTPResponse:
    # UserService automatically injected
```

**Benefits:**
- Loose coupling between components
- Easy testing with mock services
- Clean separation of concerns
- Scalable architecture patterns

### 2. **Service Layer Architecture**
```python
class TodoService:
    def create_todo(self, title: str, description: str, user_id: int) -> Todo:
        # Business logic encapsulated in service

    def get_todos(self, user_id: int | None = None) -> list[Todo]:
        # Flexible filtering logic
```

**Features:**
- Business logic separation from HTTP handling
- Reusable service methods across routes
- Consistent data operations
- Easy unit testing of business logic

### 3. **Comprehensive Input Validation**
```python
# Type conversion with error handling
try:
    user_id = int(user_id_str)
except ValueError:
    return json({"error": "User ID must be a valid integer"}, status=400)

# JSON body validation
if not request.json:
    return json({"error": "JSON body is required"}, status=400)
```

**Security Features:**
- Input sanitization and validation
- Type safety enforcement
- Detailed error messages for debugging
- Protection against malformed requests

---

## Complete API Documentation

### User Management Endpoints

#### 1. List All Users
- **URL**: `/users`
- **Method**: GET
- **Description**: Retrieve all users in the system
- **Response**: `{"users": [{"id": 1, "name": "Alice", "email": "alice@example.com"}]}`

**Example:**
```bash
curl http://localhost:8880/users
```

#### 2. Get Specific User
- **URL**: `/user?id=<user_id>`
- **Method**: GET
- **Description**: Retrieve a specific user by ID
- **Query Parameters**: `id` (required) - User ID as integer
- **Response**: `{"user": {"id": 1, "name": "Alice", "email": "alice@example.com"}}`
- **Errors**:
  - 400: Missing or invalid user ID
  - 404: User not found

**Examples:**
```bash
# Valid request
curl "http://localhost:8880/user?id=1"

# Invalid ID type
curl "http://localhost:8880/user?id=abc"

# Missing ID
curl "http://localhost:8880/user"
```

### Todo Management Endpoints

#### 3. List Todos (with Filtering)
- **URL**: `/todos`
- **Method**: GET
- **Description**: Retrieve todos, optionally filtered by user
- **Query Parameters**: `user_id` (optional) - Filter todos by user ID
- **Response**: `{"todos": [{"id": 1, "title": "Learn Python", "completed": false}]}`

**Examples:**
```bash
# All todos
curl http://localhost:8880/todos

# Todos for specific user
curl "http://localhost:8880/todos?user_id=1"
```

#### 4. Get Specific Todo
- **URL**: `/todos/<todo_id>`
- **Method**: GET
- **Description**: Retrieve a specific todo by ID
- **Parameters**: `todo_id` (int) - Todo ID in URL path
- **Response**: `{"todo": {"id": 1, "title": "Learn Python", "completed": false}}`
- **Errors**: 404 if todo not found

**Example:**
```bash
curl http://localhost:8880/todos/1
```

#### 5. Create New Todo
- **URL**: `/todo`
- **Method**: POST
- **Description**: Create a new todo item
- **Request Body**:
  ```json
  {
    "title": "Learn Sanic",
    "description": "Complete all Sanic tutorials",
    "user_id": 1
  }
  ```
- **Response**: `{"todo": {"id": 3, "title": "Learn Sanic", "completed": false}}`
- **Validation**:
  - Title and description must be non-empty strings
  - user_id must be valid integer
- **Errors**: 400 for validation failures

**Example:**
```bash
curl -X POST http://localhost:8880/todo \
  -H "Content-Type: application/json" \
  -d '{"title": "New Task", "description": "Task description", "user_id": 1}'
```

#### 6. Update Todo
- **URL**: `/todo?id=<todo_id>`
- **Method**: PUT
- **Description**: Update an existing todo
- **Query Parameters**: `id` (required) - Todo ID to update
- **Request Body**:
  ```json
  {
    "title": "Updated Title",
    "description": "Updated description",
    "completed": true
  }
  ```
- **Response**: `{"todo": {"id": 1, "title": "Updated Title", "completed": true}}`
- **Validation**: Title, description must be strings; completed must be boolean
- **Errors**: 400 for validation, 404 if todo not found

**Example:**
```bash
curl -X PUT "http://localhost:8880/todo?id=1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Task", "description": "Updated description", "completed": true}'
```

#### 7. Delete Todo
- **URL**: `/todo?id=<todo_id>`
- **Method**: DELETE
- **Description**: Delete a todo by ID
- **Query Parameters**: `id` (required) - Todo ID to delete
- **Response**: `{"message": "Todo deleted successfully"}`
- **Errors**: 400 for invalid ID, 404 if todo not found

**Example:**
```bash
curl -X DELETE "http://localhost:8880/todo?id=1"
```

#### 8. Toggle Todo Completion
- **URL**: `/todo/<todo_id>/toggle`
- **Method**: PATCH
- **Description**: Toggle the completion status of a todo
- **Parameters**: `todo_id` (int) - Todo ID in URL path
- **Response**: `{"todo": {"id": 1, "completed": true}}`
- **Errors**: 404 if todo not found

**Example:**
```bash
curl -X PATCH http://localhost:8880/todo/1/toggle
```

---

## Data Models

### User Model
```python
class User(TypedDict):
    id: int
    email: str
    name: str
```

### Todo Model
```python
class Todo(TypedDict):
    id: int
    title: str
    description: str
    completed: bool
    user_id: int
```

**Features:**
- Type safety with TypedDict
- Clear data structure definitions
- IDE support and validation
- Consistent data representation

---

## Service Architecture

### UserService
```python
class UserService:
    def get_user(self, user_id: int) -> User | None
    def get_users(self) -> list[User]
```

**Responsibilities:**
- User data management
- User lookup operations
- Data validation and formatting

### TodoService
```python
class TodoService:
    def create_todo(self, title: str, description: str, user_id: int) -> Todo
    def get_todo(self, todo_id: int) -> Todo | None
    def get_todos(self, user_id: int | None = None) -> list[Todo]
    def update_todo(self, todo_id: int, title: str, description: str, completed: bool) -> Todo | None
    def delete_todo(self, todo_id: int) -> bool
    def toggle_todo_completion(self, todo_id: int) -> Todo | None
```

**Responsibilities:**
- Todo CRUD operations
- Business logic for todo management
- Data consistency and validation
- User-specific filtering

**Advanced Features:**
- Unique ID generation with proper incrementing
- Flexible filtering (all todos or user-specific)
- Immutable data handling with TypedDict
- Comprehensive error handling

---

## Setup and Installation

### Prerequisites
```bash
# Ensure you have Python 3.8+ installed
python --version

# Install required packages
pip install -r requirements.txt
```

### Dependencies
```txt
sanic>=22.3.0
sanic-ext>=22.3.0
```

### Running the Application
```bash
# Start the development server
python main.py

# Server will start on http://localhost:8880
# Access the API endpoints immediately
```

### Configuration
```python
# In main.py
app.run(
    host="localhost",
    port=8880,
    debug=True,
    single_process=True  # Simplified for development
)
```

---

## Testing the Application

### 1. **Automated Testing Suite**
```bash
# Run comprehensive API tests
python test_app.py

# Run server health checks
python test_server.py
```

### 2. **Manual Testing Examples**

#### Test User Operations
```bash
# Get all users
curl http://localhost:8880/users

# Get specific user
curl "http://localhost:8880/user?id=1"

# Test error handling
curl "http://localhost:8880/user?id=999"  # Should return 404
curl "http://localhost:8880/user?id=abc"  # Should return 400
```

#### Test Todo Operations
```bash
# Create a new todo
curl -X POST http://localhost:8880/todo \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Todo", "description": "Test description", "user_id": 1}'

# List all todos
curl http://localhost:8880/todos

# List user-specific todos
curl "http://localhost:8880/todos?user_id=1"

# Update a todo
curl -X PUT "http://localhost:8880/todo?id=1" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Todo", "description": "Updated description", "completed": true}'

# Toggle completion
curl -X PATCH http://localhost:8880/todo/1/toggle

# Delete a todo
curl -X DELETE "http://localhost:8880/todo?id=1"
```

### 3. **Error Scenario Testing**
```bash
# Test validation errors
curl -X POST http://localhost:8880/todo \
  -H "Content-Type: application/json" \
  -d '{"title": "", "description": "Empty title"}'

# Test missing JSON body
curl -X POST http://localhost:8880/todo

# Test invalid data types
curl -X POST http://localhost:8880/todo \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", "description": "Test", "user_id": "invalid"}'
```

---

## Bug Fixes and Improvements

This tutorial includes comprehensive bug fixes identified during development:

### 1. **Type Conversion Issues**
- **Problem**: String query parameters compared with integer IDs
- **Solution**: Proper type conversion with error handling

### 2. **Function Signature Mismatches**
- **Problem**: Service methods had incorrect parameter expectations
- **Solution**: Aligned method signatures with calling code

### 3. **TypedDict Mutation Attempts**
- **Problem**: Trying to modify immutable TypedDict objects
- **Solution**: Create new objects for updates

### 4. **Missing Input Validation**
- **Problem**: No validation for request data
- **Solution**: Comprehensive input validation and error handling

### 5. **Server Startup Issues**
- **Problem**: Multiple sanic-ext initialization causing conflicts
- **Solution**: Single initialization with proper dependency management

**See [BUGFIXES_SUMMARY.md](./BUGFIXES_SUMMARY.md) for detailed explanations and code examples.**

---

## Key Learning Objectives

After completing this tutorial, you will understand:

### 1. **Service-Oriented Architecture**
- How to separate business logic from HTTP handling
- Implementing dependency injection patterns
- Creating reusable service components
- Managing service lifecycle and dependencies

### 2. **Advanced API Design**
- Comprehensive input validation strategies
- Error handling and user-friendly error messages
- Consistent API response patterns
- RESTful endpoint design principles

### 3. **Data Management Patterns**
- Working with TypedDict for type safety
- Immutable data handling techniques
- In-memory data persistence patterns
- Data filtering and querying strategies

### 4. **Testing and Quality Assurance**
- Writing comprehensive test suites
- Testing error scenarios and edge cases
- Server health checking and monitoring
- Documentation-driven development

### 5. **Production Readiness**
- Error handling and logging best practices
- Input sanitization and security considerations
- Performance optimization techniques
- Maintainable code organization

---

## Advanced Patterns Demonstrated

### 1. **Dependency Injection**
```python
# Clean, testable architecture
async def create_todo(request: Request, todo_service: TodoService) -> HTTPResponse:
    # Service automatically injected, easy to mock for testing
```

### 2. **Service Layer Pattern**
```python
# Business logic separated from HTTP concerns
class TodoService:
    def create_todo(self, title: str, description: str, user_id: int) -> Todo:
        # Pure business logic, no HTTP dependencies
```

### 3. **Type Safety**
```python
# Strong typing throughout the application
def get_user(self, user_id: int) -> User | None:
    # Clear contracts and IDE support
```

### 4. **Error Handling Patterns**
```python
# Consistent error responses
if not user:
    return json({"error": "User not found"}, status=404)
```

---

## Extending the Application

### 1. **Database Integration**
Replace in-memory storage with database:
```python
class TodoService:
    async def create_todo(self, title: str, description: str, user_id: int) -> Todo:
        # Add database persistence
        async with db.transaction():
            todo_id = await db.execute("INSERT INTO todos ...")
            return await self.get_todo(todo_id)
```

### 2. **Authentication**
Add JWT authentication:
```python
@app.middleware("request")
async def auth_middleware(request):
    if request.path.startswith("/api/"):
        # Validate JWT token
        user = validate_token(request.headers.get("Authorization"))
        request.ctx.user = user
```

### 3. **Validation Schemas**
Add formal validation:
```python
from dataclasses import dataclass

@dataclass
class CreateTodoRequest:
    title: str
    description: str
    user_id: int

@app.post("/todo")
@validate(json=CreateTodoRequest)
async def create_todo(request: Request, body: CreateTodoRequest):
    # Automatic validation and type conversion
```

### 4. **Pagination**
Add pagination support:
```python
async def get_todos(self, user_id: int = None, limit: int = 10, offset: int = 0):
    # Implement pagination logic
    return todos[offset:offset + limit]
```

---

## Performance Considerations

### 1. **Memory Management**
- In-memory storage suitable for development/small applications
- Consider database persistence for production use
- Implement proper cleanup for long-running applications

### 2. **Request Processing**
- Efficient validation with early returns
- Minimal object creation in hot paths
- Proper error handling without exceptions in normal flow

### 3. **Service Architecture**
- Services are singleton instances (shared across requests)
- Thread-safe operations for concurrent access
- Efficient data structures for common operations

---

## Security Considerations

### 1. **Input Validation**
- All user input validated before processing
- Type checking prevents injection attacks
- Detailed error messages for debugging (safe in development)

### 2. **Data Integrity**
- ID generation prevents conflicts
- Immutable data structures prevent accidental modifications
- Consistent data validation across all endpoints

### 3. **Error Handling**
- No sensitive information leaked in error messages
- Consistent error response format
- Proper HTTP status codes for different scenarios

---

## Next Steps and Advanced Topics

### 1. **Production Deployment**
- Add proper logging and monitoring
- Implement rate limiting and throttling
- Set up health checks and metrics
- Configure proper error reporting

### 2. **Advanced Features**
- Real-time updates with WebSockets
- Background task processing
- Caching strategies for performance
- API versioning and backward compatibility

### 3. **Testing and Quality**
- Unit tests for service layer
- Integration tests for API endpoints
- Performance testing and benchmarking
- Code coverage and quality metrics

### 4. **Architecture Evolution**
- Microservices decomposition
- Event-driven architecture patterns
- CQRS and event sourcing
- Horizontal scaling strategies

---

## Troubleshooting

### Common Issues

#### 1. **Service Injection Failures**
```python
# Ensure services are properly registered
ext.add_dependency(UserService)
ext.add_dependency(TodoService)
```

#### 2. **Type Validation Errors**
```python
# Check input types before processing
if not isinstance(user_id_value, (int, str)):
    return json({"error": "Invalid user_id type"}, status=400)
```

#### 3. **Server Startup Issues**
```python
# Use single process mode for development
app.run(host="localhost", port=8880, single_process=True)
```

#### 4. **Import Circular Dependencies**
```python
# Structure imports properly
# services.py should not import from routes.py
# types.py should be independent
```

---

## Conclusion

Day 6 represents a comprehensive Todo API implementation that demonstrates professional-grade Sanic development practices. The tutorial covers:

- **Service-oriented architecture** with dependency injection
- **Comprehensive API design** with full CRUD operations
- **Production-quality validation** and error handling
- **Testing infrastructure** for reliability and maintenance
- **Bug fixes and best practices** learned from real development

This tutorial provides a solid foundation for building scalable, maintainable APIs with Sanic. The patterns and practices demonstrated here are directly applicable to production applications and provide a strong base for further development.

### Key Achievements:
- ✅ Complete Todo API with all CRUD operations
- ✅ Service layer architecture with dependency injection
- ✅ Comprehensive input validation and error handling
- ✅ Full testing suite with automated and manual testing
- ✅ Production-ready code organization and patterns
- ✅ Detailed documentation and troubleshooting guides

The knowledge gained from this tutorial enables you to build robust, scalable APIs with confidence and follow industry best practices for API development with Sanic.

Happy coding with Sanic Todo APIs!
