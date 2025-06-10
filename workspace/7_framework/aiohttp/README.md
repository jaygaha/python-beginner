# Notes API with `aiohttp`

A simple REST API for managing notes built with Python's `aiohttp` framework. This project demonstrates the basics of building asynchronous web applications with `aiohttp`.

## 📚 What is `aiohttp`?

`aiohttp` is an asynchronous HTTP client/server framework for Python. It's built on top of asyncio and provides:
- High performance due to its asynchronous nature
- Support for both client and server-side HTTP
- WebSocket support
- Easy-to-use routing system
- Built-in JSON handling

## 🚀 Project Overview

This project implements a complete CRUD (Create, Read, Update, Delete) API for managing notes. Each note has:
- **ID**: Unique identifier (UUID)
- **Title**: Note title
- **Content**: Note content
- **Created At**: Timestamp when note was created
- **Updated At**: Timestamp when note was last modified

## 📁 Project Structure

```
aiohttp/
├── app.py                    # Main application and routes
├── models.py                 # Data models and business logic
├── notes_handler.py          # Request handlers for notes
├── default_handler.py        # Default/health check handler
├── requirements.txt          # Python dependencies
├── .style.yapf              # Code formatting configuration
├── postman_python-aiohttp.json  # Postman collection for testing
└── README.md                # This file
```

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

The server will start on `http://127.0.0.1:8070`

## 📋 API Endpoints

### Health Check
- **GET** `/` - Check if server is running

### Notes Management
- **GET** `/notes` - Get all notes
- **GET** `/notes/{id}` - Get a specific note by ID
- **POST** `/notes` - Create a new note
- **PUT** `/notes/{id}` - Update an existing note
- **DELETE** `/notes/{id}` - Delete a note

## 🔧 API Usage Examples

### 1. Health Check
```bash
curl http://localhost:8070/
```

### 2. Create a Note
```bash
curl -X POST http://localhost:8070/notes \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Note",
    "content": "This is the content of my first note"
  }'
```

### 3. Get All Notes
```bash
curl http://localhost:8070/notes
```

### 4. Get Specific Note
```bash
curl http://localhost:8070/notes/{note-id}
```

### 5. Update a Note
```bash
curl -X PUT http://localhost:8070/notes/{note-id} \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Note Title",
    "content": "Updated content"
  }'
```

### 6. Delete a Note
```bash
curl -X DELETE http://localhost:8070/notes/{note-id}
```

## 📝 Code Explanation

### app.py - Main Application
This file contains:
- Application setup with `web.Application()`
- Route definitions using `app.router.add_*()` methods
- Server configuration

### models.py - Data Layer
Contains:
- In-memory storage for notes (using Python dictionary)
- CRUD functions for note operations
- UUID generation for unique IDs
- Datetime handling for timestamps

### notes_handler.py - Request Handlers
Implements async functions that:
- Handle HTTP requests
- Validate input data
- Call model functions
- Return JSON responses with appropriate status codes

### default_handler.py - Utility Handlers
Simple handler for health checks and default responses.

## 🧪 Testing with Postman

The project includes a Postman collection (`postman_python-aiohttp.json`) with pre-configured requests for all endpoints. Import this file into Postman to test the API easily.

## 🎯 Key Learning Points

### 1. Async/Await Pattern
```python
async def create_note_handler(request):
    data = await request.json()  # Async operation
    # ... rest of the function
```

### 2. Route Parameter Extraction
```python
note_id = request.match_info.get("id")  # Extract {id} from URL
```

### 3. JSON Request/Response Handling
```python
data = await request.json()  # Parse JSON request
return web.json_response(note)  # Return JSON response
```

### 4. HTTP Status Codes
```python
return web.json_response(note, status=201)  # Created
return web.json_response({"error": "Not found"}, status=404)  # Not Found
```

## 🚨 Important Notes

- **Data Persistence**: This project uses in-memory storage. All data is lost when the server restarts.
- **Production Ready**: This is a learning project. For production, you'd need:
  - Proper database integration
  - Authentication and authorization
  - Input validation and sanitization
  - Error logging
  - CORS handling
  - Rate limiting

## 🔄 Next Steps

To extend this project, consider:
1. Adding database support (PostgreSQL, MongoDB)
2. Implementing user authentication
3. Adding input validation with libraries like marshmallow
4. Writing unit tests
5. Adding API documentation with Swagger
6. Implementing search and filtering
7. Adding file upload capabilities

## 📚 Further Learning

- [aiohttp Documentation](https://docs.aiohttp.org/)
- [Python asyncio](https://docs.python.org/3/library/asyncio.html)
- [RESTful API Design](https://restfulapi.net/)
- [HTTP Status Codes](https://httpstatuses.com/)

## 🤝 Contributing

This is a learning project! Feel free to:
- Add new features
- Improve error handling
- Add tests
- Enhance documentation

Happy coding! 🎉
