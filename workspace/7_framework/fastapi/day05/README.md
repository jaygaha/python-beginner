# FastAPI Day 05: HTTP Status Codes and Error Handling

Welcome to **Day 05** of the FastAPI tutorial! Today you'll learn how to handle HTTP status codes, create custom error responses, and manage exceptions in your API endpoints.

---

## What You'll Learn

- How to use and return appropriate HTTP status codes
- How to create and use custom exception classes
- How to handle validation and business logic errors gracefully
- How to implement global exception handlers for consistent error responses
- How to write automated tests for error handling

---

## Key Concepts

### 1. HTTP Status Codes

- **HTTP status codes** communicate the result of an API request.
- Use codes like `200 OK`, `201 Created`, `404 Not Found`, `409 Conflict`, `422 Unprocessable Entity`, and `500 Internal Server Error` to indicate different outcomes.

Example status codes:
```
201 Created - When a new item or order is successfully created
404 Not Found - When a requested resource does not exist
409 Conflict - When there is a duplicate or business logic conflict
422 Unprocessable Entity - When validation fails
500 Internal Server Error - For unexpected errors
```

### 2. Custom Exception Classes

- Define custom exception classes for common error scenarios (e.g., not found, insufficient stock, duplicate item).
- Inherit from FastAPI's `HTTPException` for easy integration.

Example custom exception:
```
class ItemNotFoundError(HTTPException):
    def __init__(self, item_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
```

### 3. Exception Handlers

- Use FastAPI's `@app.exception_handler` to create global handlers for your custom exceptions.
- Return structured error responses with details, error type, and timestamps.

Example handler:
```
@app.exception_handler(ItemNotFoundError)
async def item_not_found_handler(request: Request, exc: ItemNotFoundError):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Item Not Found",
            "message": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )
```

### 4. Validation and Business Logic Errors

- Use Pydantic for request validation and raise custom errors for business logic issues (e.g., insufficient stock, invalid transitions).
- Customize error responses for better client experience.

Example validation error:
```
@app.exception_handler(RequestValidationError)
async def request_validation_error_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": "Invalid request data",
            "details": exc.errors(),
            "timestamp": datetime.now().isoformat(),
            "path": str(request.url.path)
        }
    )
```

### 5. Logging and Monitoring

- Use Python's `logging` module to log errors and important events.
- Logging helps with debugging and monitoring your API in production.

---

## Next Steps

- Try sending requests that trigger different error scenarios (e.g., not found, duplicate, validation errors).
- Explore the code to see how exceptions and handlers are implemented.
- Run the tests to ensure error handling works as expected!

---

**Tip:** FastAPI’s automatic docs are available at `/api/docs` when you run your app.

---