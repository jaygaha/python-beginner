# Sanic Web Framework

Sanic is a Python web framework and web server that's written to go fast. It allows the usage of the `async/await` syntax added in Python 3.5, which makes your code non-blocking and speedy.

## What is Sanic?

Sanic is an async Python web framework that is designed to be fast and simple. It's similar to Flask but built specifically for async/await syntax and high performance applications.

### Key Features

- **Async/Await Support**: Built from the ground up to support Python's async/await syntax
- **Fast Performance**: Designed for speed with minimal overhead
- **Flask-like Syntax**: Familiar decorator-based routing system
- **Built-in Server**: Comes with its own high-performance server
- **WebSocket Support**: Native WebSocket support for real-time applications
- **Middleware Support**: Extensible middleware system for request/response processing
- **Static File Serving**: Built-in static file serving capabilities
- **JSON Responses**: First-class support for JSON API development

## Why Use Sanic?

### Performance
- **High Throughput**: Can handle thousands of requests per second
- **Low Latency**: Minimal request processing overhead
- **Async I/O**: Non-blocking I/O operations for better resource utilization

### Developer Experience
- **Simple API**: Easy to learn, especially if you know Flask
- **Hot Reload**: Automatic reloading during development
- **Comprehensive Documentation**: Well-documented with examples
- **Active Community**: Strong community support and regular updates

### Use Cases
- **REST APIs**: Perfect for building high-performance REST APIs
- **Microservices**: Ideal for microservice architectures
- **Real-time Applications**: WebSocket support for real-time features
- **High-Traffic Applications**: Designed to handle high concurrent loads

## Installation

```bash
pip install sanic
```

## Basic Example

```python
from sanic import Sanic
from sanic.response import json

app = Sanic("MyApp")

@app.route("/")
async def test(request):
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

## Project Structure

This directory contains various Sanic tutorials and examples:

```
sanic/
├── day1_basic/              # Basic Sanic implementation
│   ├── app/
│   │   ├── __init__.py
│   │   └── routes.py
│   ├── main.py
│   └── README.md
├── day2_intermediate/       # Intermediate Sanic concepts
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── api_blueprint.py
│   │   └── error_handlers.py
│   ├── main.py
│   └── README.md
├── day3_sqlite/             # Advanced Sanic with database integration
│   ├── app/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── database.py
│   │   ├── error_handlers.py
│   │   └── config.py
│   ├── main.py
│   ├── requirements.txt
│   └── README.md
└── README.md          # This file
```

## Core Concepts

### 1. Application Instance
```python
from sanic import Sanic
app = Sanic("MyApp")
```

### 2. Route Decorators
```python
@app.route("/path")
@app.route("/path", methods=["GET", "POST"])
@app.route("/path/<param>")
```

### 3. Async Handlers
```python
@app.route("/")
async def handler(request):
    return response
```

### 4. Request Object
- `request.json()` - Parse JSON body
- `request.args` - Query parameters
- `request.form` - Form data
- `request.files` - Uploaded files

### 5. Response Types
- `text()` - Plain text response
- `json()` - JSON response
- `html()` - HTML response
- `file()` - File response
- `redirect()` - Redirect response

## Performance Comparison

Sanic is designed for speed. Here's how it compares to other Python frameworks:

| Framework | Requests/sec | Relative Speed | Use Case |
|-----------|-------------|----------------|----------|
| Sanic     | ~40,000     | 1.0x          | High-performance APIs, real-time apps |
| FastAPI   | ~30,000     | 0.75x         | Modern APIs with auto-documentation |
| Flask     | ~5,000      | 0.125x        | Simple web apps, prototyping |
| Django    | ~3,000      | 0.075x        | Full-featured web applications |

*Note: Performance varies based on application complexity and server configuration*

### Day 3 Performance Features
- **Database Connection Pooling**: Efficient async SQLite operations
- **HTTP Client Optimization**: Connection reuse and timeout management
- **Memory Management**: Proper resource cleanup and cursor handling
- **Configuration Caching**: Environment-based settings loaded once

## When to Use Sanic

### Good For:
- High-performance APIs
- Real-time applications
- Microservices
- Applications requiring async I/O
- CPU-intensive tasks with async operations

### Consider Alternatives For:
- Simple CRUD applications (Flask might be simpler)
- Applications requiring extensive ORM features (Django)
- Applications with heavy synchronous processing

## Learning Path

1. **Start with Basic** - Explore the `day1_basic/` directory
2. **Understand Async** - Learn Python's async/await syntax
3. **Practice Routing** - Try different route patterns
4. **Learn Intermediate Concepts** - Explore the `day2_intermediate/` directory
5. **Add Middleware** - Implement request/response processing
6. **Master Advanced Features** - Explore the `day3_sqlite/` directory
7. **Database Integration** - Learn async SQLite operations and data persistence
8. **External Service Integration** - Make HTTP requests to external APIs
9. **Configuration Management** - Implement environment-based configuration
10. **Production Deployment** - Learn deployment strategies and monitoring

## Resources

- **Official Documentation**: https://sanic.dev/
- **GitHub Repository**: https://github.com/sanic-org/sanic
- **Community Discord**: https://discord.gg/FARQzAE
- **PyPI Package**: https://pypi.org/project/sanic/

## Version Information

The examples in this directory use Sanic 22.3.0, which provides:
- Stable async/await support
- Comprehensive middleware system
- WebSocket support
- Static file serving
- JSON request/response handling

## Tutorial Structure

### Day 1 - Basic Concepts (`day1_basic/`)
- Basic routing and HTTP methods
- JSON and text responses
- URL parameters and request handling
- Async programming fundamentals
- Simple application structure

### Day 2 - Intermediate Concepts (`day2_intermediate/`)
- Middleware for request/response processing
- Error handling and custom error responses
- Blueprints for organizing routes
- Application lifecycle listeners
- Multi-worker deployment

### Day 3 - Advanced Features (`day3_sqlite/`)
- **Query Parameters**: Handle URL query parameters with validation
- **Typed Route Parameters**: Automatic type conversion and validation
- **JSON Validation**: Robust request body validation with detailed error messages
- **Async HTTP Client**: External API calls with httpx and comprehensive error handling
- **Async SQLite Integration**: Complete database operations with aiosqlite
- **Configuration Management**: Environment-based configuration with dataclasses
- **Enhanced Logging**: Structured logging throughout the application
- **Production Patterns**: Error handling, resource management, and security best practices

## Getting Started

1. **Begin with Day 1**: Navigate to the `day1_basic/` directory
2. Follow the setup instructions in `day1_basic/README.md`
3. Run the example application and test all endpoints
4. **Progress to Day 2**: Navigate to the `day2_intermediate/` directory
5. Follow the setup instructions in `day2_intermediate/README.md`
6. Explore middleware, error handling, and blueprints
7. **Advance to Day 3**: Navigate to the `day3_sqlite/` directory
8. Follow the setup instructions in `day3_sqlite/README.md`
9. Learn database integration, external APIs, and advanced validation
10. Practice with query parameters, typed routes, and JSON validation
11. Experiment with the configuration system and logging
12. Test all endpoints and error handling scenarios

## Tutorial Progression Comparison

| Feature | Day 1 | Day 2 | Day 3 |
|---------|-------|-------|-------|
| **Routing** | Basic GET/POST | Blueprints | Query params, typed routes |
| **Responses** | Text, JSON | Custom headers | Enhanced validation |
| **Error Handling** | Basic exceptions | Centralized handlers | Comprehensive logging |
| **Architecture** | Simple structure | Middleware, listeners | Configuration management |
| **Data Storage** | In-memory | None | Async SQLite database |
| **External Services** | None | None | HTTP client with httpx |
| **Configuration** | Hardcoded | Basic setup | Environment-based |
| **Logging** | Print statements | Basic logging | Structured logging |
| **Production Ready** | Development only | Multi-worker | Full production patterns |
| **Complexity** | Beginner | Intermediate | Advanced |

### Learning Path Summary

- **Day 1**: Master the fundamentals of Sanic routing, responses, and async concepts
- **Day 2**: Learn application organization with middleware, blueprints, and error handling
- **Day 3**: Build production-ready applications with databases, external APIs, and proper configuration

Each tutorial builds upon the previous one, creating a comprehensive learning experience that takes you from basic concepts to advanced production patterns.

Happy coding with Sanic!
