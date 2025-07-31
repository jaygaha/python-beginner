# FastAPI Day 03: Path Parameters and Query Parameters

Welcome to **Day 03** of the FastAPI tutorial! Today you'll learn how to handle user requests with path parameters, query parameters, and write automated tests.

---

## What You'll Learn

- How to validate path parameters
- How to define and validate query parameters
- How to use Enums for restricted values
- How to handle complex query parameters
- How to write automated tests for these features

---

## Key Concepts

### 1. Path Parameters

- **Path parameters** are part of the URL path and are used to identify specific resources.
- FastAPI allows you to validate path parameters using types and constraints.

Example path parameter:
```
GET /users/{user_id}
```

### 2. Query Parameters

- **Query parameters** are key-value pairs appended to the URL after a `?`.
- FastAPI supports validation for query parameters, including types, ranges, and patterns.

Example query parameters:
```
GET /users?status=active&sort_by=age
```

### 3. Enums for Restricted Values

- Use Python's `Enum` to restrict query or path parameters to specific values.

Example:
```python
class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
```

### 4. Complex Query Parameters

- FastAPI allows you to handle more complex query parameters, such as filtering, sorting, and pagination.

---

## Next Steps

- Try sending requests to your API with different path and query parameters.
- Explore the code to see how validation and filtering are implemented.
- Run the tests to ensure everything works as expected!

---

**Tip:** FastAPI’s automatic docs are available at `/docs` when you run your app.

---
