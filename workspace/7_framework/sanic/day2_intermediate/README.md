# Sanic Intermediate Tutorial — Day 2

An intermediate Sanic web framework tutorial covering middleware, error handling, blueprints, application listeners, and multi-worker deployment.

---

## Project Structure

```
day2_intermediate/
├── app/
│   ├── __init__.py          # App initialization with middleware and listeners
│   ├── routes.py            # Basic standalone routes
│   ├── api_blueprint.py     # Blueprint for API routes
│   └── error_handlers.py    # Centralized error handling
├── main.py                  # Application entry point with multi-worker setup
├── requirements.txt         # Dependencies
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

The server will start on `http://localhost:8880` with 4 worker processes.

---

## New Concepts Covered

### 1. Middleware
Middleware functions that run before and after each request to add functionality like logging, authentication, or response modification.

### 2. Error Handling
Centralized error handling for different types of exceptions with custom error responses.

### 3. Blueprints
Organize routes into logical groups using blueprints for better code organization and modularity.

### 4. Application Listeners
Lifecycle event handlers that run during application startup, shutdown, and other events.

### 5. Multi-Worker Deployment
Running the application with multiple worker processes for better performance and scalability.

---

## API Endpoints

### Basic Routes

#### 1. Home Route
- **URL**: `/`
- **Method**: GET
- **Description**: Returns a simple text greeting
- **Response**: Plain text "Hello, Sanic World!"

**Example:**
```bash
curl http://localhost:8880/
```

### Blueprint Routes (API)

#### 2. Status Check
- **URL**: `/api/status`
- **Method**: GET
- **Description**: Returns application status
- **Response**: `{"status": "running"}`

**Example:**
```bash
curl http://localhost:8880/api/status
```

#### 3. User Greeting
- **URL**: `/api/user/<name>`
- **Method**: GET
- **Description**: Returns a personalized greeting for the specified user
- **Parameters**: `name` (string) - The user's name
- **Response**: `{"message": "Hello, {name}!"}`

**Example:**
```bash
curl http://localhost:8880/api/user/John
```

### Error Handling Examples

#### 4. 404 Error
- **URL**: `/nonexistent`
- **Method**: GET
- **Description**: Demonstrates custom 404 error handling
- **Response**: `{"error": "Route not found!"}` (Status: 404)

**Example:**
```bash
curl http://localhost:8880/nonexistent
```

---

## Code Features Demonstrated

### 1. Request Middleware
```python
@app.middleware("request")
async def print_request(request):
    print(f"Request: {request.method} {request.path}")
```

**Features:**
- Logs every incoming request
- Runs before route handlers
- Access to request object

### 2. Response Middleware
```python
@app.middleware("response")
async def add_custom_header(request, response):
    response.headers["X-Powered-By"] = "Sanic Tutorial"
```

**Features:**
- Modifies outgoing responses
- Adds custom headers
- Runs after route handlers

### 3. Error Handlers
```python
@app.exception(NotFound)
async def not_found(request, exception):
    return json({"error": "Route not found!"}, status=404)
```

**Features:**
- Custom 404 error responses
- Generic exception handling
- Consistent error response format

### 4. Blueprint Organization
```python
api = Blueprint("api", url_prefix="/api")

@api.route("/status")
async def status(request):
    return json({"status": "running"})
```

**Features:**
- URL prefix for grouped routes
- Logical route organization
- Modular code structure

### 5. Application Listeners
```python
@app.listener("after_server_stop")
async def shutdown(app, loop):
    print("Server stopped, cleaning up resources.")
```

**Features:**
- Lifecycle event handling
- Resource cleanup
- Application state management

---

## Key Concepts

### Middleware Types
- **Request Middleware**: Runs before route handlers
- **Response Middleware**: Runs after route handlers
- **Exception Middleware**: Handles exceptions during request processing

### Error Handling Strategy
- **Specific Exception Handlers**: Handle particular exceptions (e.g., NotFound)
- **Generic Exception Handler**: Catch-all for unhandled exceptions
- **Consistent Response Format**: Standardized error response structure

### Blueprint Benefits
- **Code Organization**: Group related routes together
- **URL Prefixing**: Automatic URL prefix application
- **Modularity**: Separate concerns into different modules
- **Reusability**: Blueprints can be reused across applications

### Application Lifecycle
- **before_server_start**: Initialize resources before server starts
- **after_server_start**: Setup complete, server is ready
- **before_server_stop**: Cleanup before server stops
- **after_server_stop**: Final cleanup after server stops

### Multi-Worker Deployment
- **Performance**: Multiple processes handle requests concurrently
- **Scalability**: Better resource utilization
- **Fault Tolerance**: Worker process failures don't affect others
- **Configuration**: `workers=4` parameter in `app.run()`

---

## Testing the Features

### 1. Test Middleware
Watch the console output when making requests - you'll see request logging from the middleware.

### 2. Test Error Handling
```bash
# Test 404 error
curl http://localhost:8880/nonexistent

# Response headers show custom middleware
curl -I http://localhost:8880/api/status
```

### 3. Test Blueprint Routes
```bash
# All API routes have /api prefix
curl http://localhost:8880/api/status
curl http://localhost:8880/api/user/Jay
```

### 4. Test Application Lifecycle
Stop the server (Ctrl+C) and observe the shutdown message from the listener.

---

## Performance Considerations

### Multi-Worker Benefits
- **Increased Throughput**: Multiple processes handle requests simultaneously
- **Better Resource Utilization**: Takes advantage of multiple CPU cores
- **Improved Fault Tolerance**: Individual worker failures don't crash the entire application

### Middleware Performance
- **Request Middleware**: Adds minimal overhead for logging and preprocessing
- **Response Middleware**: Efficient header manipulation
- **Keep It Light**: Avoid heavy processing in middleware

### Blueprint Efficiency
- **Route Organization**: No performance impact, purely organizational
- **URL Prefix**: Efficiently handled by Sanic's routing system
- **Memory Usage**: Minimal additional memory overhead

---

## Best Practices

### 1. Middleware Design
- Keep middleware functions lightweight
- Use async/await for I/O operations
- Handle exceptions gracefully
- Order middleware appropriately

### 2. Error Handling
- Provide meaningful error messages
- Use appropriate HTTP status codes
- Log errors for debugging
- Don't expose internal details

### 3. Blueprint Organization
- Group related functionality together
- Use descriptive blueprint names
- Keep URL prefixes consistent
- Separate concerns clearly

### 4. Application Lifecycle
- Use listeners for resource management
- Clean up resources properly
- Handle graceful shutdowns
- Initialize dependencies correctly

---

## Next Steps

After completing this tutorial, you should understand:
- How to implement middleware for request/response processing
- How to handle errors centrally with custom responses
- How to organize routes using blueprints
- How to manage application lifecycle events
- How to deploy with multiple workers

### Recommended Next Topics:
1. **Database Integration**: Connect to databases with async drivers
2. **Authentication**: Implement JWT or session-based authentication
3. **Testing**: Write unit and integration tests
4. **WebSockets**: Add real-time functionality
5. **Production Deployment**: Deploy with proper configuration

---

## Troubleshooting

### Common Issues:
1. **Port Already in Use**: Change the port in `main.py`
2. **Worker Process Errors**: Reduce worker count or check system resources
3. **Middleware Order**: Ensure middleware is registered before routes
4. **Blueprint Registration**: Make sure blueprints are registered with the app

### Debug Mode:
The application runs in debug mode by default. For production, set `debug=False` in `main.py`.

---

Happy coding with Sanic!
