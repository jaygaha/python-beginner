# FastAPI Day 02: Request & Response Models, Validation, and Testing

Welcome to **Day 02** of the FastAPI tutorial! Today you'll learn how to handle user data with request and response models, validate input, build basic CRUD endpoints, and write automated tests.

---

## What You'll Learn

- How to define request and response models using Pydantic
- How FastAPI automatically validates incoming data
- How to create, read, and update user records (CRUD)
- How to write simple automated tests for your API

---

## Key Concepts

### 1. Request & Response Models

- **Request models** define the shape of data clients send to your API (e.g., when creating a user).
- **Response models** define what your API returns (e.g., user info, without the password).

Example request (to create a user):

```json
{
  "username": "code.conductor",
  "email": "jay@example.com",
  "full_name": "Jay",
  "password": "supersecret",
  "age": 25
}
```

Example response (after creating a user):

```json
{
  "id": 1,
  "username": "code.conductor",
  "email": "jay@example.com",
  "full_name": "Jay",
  "age": 25,
  "is_active": true,
  "created_at": "2025-07-30T12:00:00"
}
```

### 2. Automatic Validation

- FastAPI uses Pydantic to check types, lengths, and formats.
- Invalid data (like a short username or bad email) gets rejected automatically.

### 3. CRUD Endpoints

- **Create**: Add a new user (`POST /users`)
- **Read**: Get all users (`GET /users`), or a single user by ID (`GET /users/{id}`)
- **Update**: Change user info (`PUT /users/{id}`)

### 4. Automated Testing

- Tests check that your API works as expected.
- You’ll see how to test user creation, validation errors, and updates.

---

## Next Steps

- Try sending requests to your API and see how validation works.
- Explore the code to see how models and endpoints are defined.
- Run the tests to make sure everything works!

---

**Tip:** FastAPI’s automatic docs are available at `/docs` when you run your app.

---
