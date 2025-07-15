# Sanic Beginner Tutorial — Day 1

A beginner-friendly Sanic web framework tutorial covering basic routing, JSON responses, URL parameters, POST requests, and async handling.

**Prerequisites:** Basic Python knowledge and understanding of web concepts.

**Next Tutorial:** After completing this tutorial, continue with [Day 2 - Intermediate Concepts](../day2_intermediate/README.md) to learn about middleware, error handling, blueprints, and application listeners.

---

## Project Structure

```
day1_basic/
├── app/
│   ├── __init__.py      # App initialization and configuration
│   └── routes.py        # All route definitions
├── main.py              # Application entry point
├── requirements.txt     # Dependencies
└── README.md           # This file
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

The server will start on `http://localhost:8880`

---

## API Endpoints

### 1. Home Route
- **URL**: `/`
- **Method**: GET
- **Description**: Returns a simple text greeting
- **Response**: Plain text "Hello, Sanic world!"

**Example:**
```bash
curl http://localhost:8880/
```

### 2. JSON Greeting
- **URL**: `/api/greet`
- **Method**: GET
- **Description**: Returns a JSON greeting message
- **Response**: `{"message": "Hello, Sanic API!"}`

**Example:**
```bash
curl http://localhost:8880/api/greet
```

### 3. User Greeting with URL Parameter
- **URL**: `/api/user/<name>`
- **Method**: GET
- **Description**: Returns a personalized greeting for the specified user
- **Parameters**: `name` (string) - The user's name
- **Response**: `{"message": "Hello, user {name}!"}`

**Example:**
```bash
curl http://localhost:8880/api/user/John
```

### 4. Create User (POST)
- **URL**: `/api/user`
- **Method**: POST
- **Description**: Creates a new user with the provided name
- **Request Body**: JSON with `name` field
- **Response**: `{"message": "User {name} created!"}`

**Example:**
```bash
curl -X POST http://localhost:8880/api/user \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice"}'
```

### 5. Async Demo
- **URL**: `/api/wait`
- **Method**: GET
- **Description**: Demonstrates async functionality with a 2-second delay
- **Response**: `{"message": "Async demo completed! Waited for 2 seconds asynchronously!"}`

**Example:**
```bash
curl http://localhost:8880/api/wait
```

---

## Code Features Demonstrated

### 1. Basic Routing
- Simple route definitions using `@app.route()` decorator
- Different HTTP methods (GET, POST)

### 2. Response Types
- **Text responses**: Using `text()` for plain text
- **JSON responses**: Using `json()` for structured data

### 3. URL Parameters
- Dynamic route parameters: `/api/user/<name>`
- Accessing parameters in handler functions

### 4. Request Handling
- Processing JSON request bodies
- Async request handling with `await request.json()`

### 5. Async Programming
- Async route handlers
- Non-blocking operations with `asyncio.sleep()`

---

## Key Concepts

### App Structure
- **App Instance**: Created in `app/__init__.py` as `Sanic("SanicBasicApp")`
- **Route Organization**: All routes defined in `app/routes.py`
- **Entry Point**: `main.py` handles app startup with configuration

### Async Nature
- All route handlers are async functions
- Sanic is built for high-performance async operations
- Demonstrates non-blocking I/O with the `/api/wait` endpoint

### Configuration
- Server runs on `0.0.0.0:8880`
- Debug mode enabled for development
- Hot reload available in debug mode

---

## What You've Learned

After completing this tutorial, you should understand:
- How to create a basic Sanic application
- How to define routes with different HTTP methods
- How to handle URL parameters and request data
- How to return different response types (text, JSON)
- How to work with async/await in Sanic
- How to structure a simple Sanic application

## Next Steps

### Ready for Day 2?
Continue your Sanic journey with [Day 2 - Intermediate Concepts](../day2_intermediate/README.md), which covers:
- **Middleware**: Request/response processing
- **Error Handling**: Custom error responses
- **Blueprints**: Route organization
- **Application Listeners**: Lifecycle events
- **Multi-Worker Deployment**: Performance optimization

### Additional Practice Ideas:
1. Add more complex URL parameters (e.g., `/api/user/<user_id:int>`)
2. Implement query parameter handling
3. Add file upload functionality
4. Create a simple REST API for a resource
5. Add request validation

---

## Troubleshooting

### Common Issues:
1. **Port Already in Use**: Change the port number in `main.py`
2. **Module Import Errors**: Ensure you're running from the correct directory
3. **JSON Parsing Errors**: Check request Content-Type header
4. **Async/Await Confusion**: Remember all route handlers must be async

### Debug Tips:
- Use `print()` statements to debug request data
- Check the console for error messages
- Use a tool like Postman or curl to test endpoints
- Enable debug mode for detailed error information

---
