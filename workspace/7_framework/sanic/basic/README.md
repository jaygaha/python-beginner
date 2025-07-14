# Sanic Beginner Tutorial — Day 1

A beginner-friendly Sanic web framework tutorial covering basic routing, JSON responses, URL parameters, POST requests, and async handling.

---

## Project Structure

```
basic/
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
