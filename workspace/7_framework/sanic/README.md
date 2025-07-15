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

| Framework | Requests/sec | Relative Speed |
|-----------|-------------|----------------|
| Sanic     | ~40,000     | 1.0x          |
| FastAPI   | ~30,000     | 0.75x         |
| Flask     | ~5,000      | 0.125x        |
| Django    | ~3,000      | 0.075x        |

*Note: Performance varies based on application complexity and server configuration*

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
6. **Database Integration** - Connect to databases with async drivers
7. **Production Deployment** - Learn deployment strategies

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

## Getting Started

1. **Begin with Day 1**: Navigate to the `day1_basic/` directory
2. Follow the setup instructions in `day1_basic/README.md`
3. Run the example application and test all endpoints
4. **Progress to Day 2**: Navigate to the `day2_intermediate/` directory
5. Follow the setup instructions in `day2_intermediate/README.md`
6. Explore middleware, error handling, and blueprints
7. Experiment with the code to understand how it works

Happy coding with Sanic!
