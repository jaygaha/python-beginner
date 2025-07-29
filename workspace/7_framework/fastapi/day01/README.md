# FastAPI Day 01 Tutorial

Welcome to **Day 01** of the FastAPI tutorial series! This session introduces the basics of building a simple REST API using FastAPI, including endpoint creation and automated testing.

---

## Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [How to Run](#how-to-run)
- [Testing](#testing)
- [Requirements](#requirements)

---

## Overview

This tutorial demonstrates how to:

- Set up a FastAPI application.
- Create basic GET endpoints.
- Return JSON responses.
- Write and run automated tests using `pytest` and FastAPI's `TestClient`.

---

## Project Structure

```
src/
  main.py           # FastAPI application with endpoints
tests/
  test_main.py      # Unit tests for the API
requirements.txt    # Python dependencies
pytest.ini          # Pytest configuration
README.md           # This file
```

---

## API Endpoints

### 1. Root Endpoint

- **URL:** `/`
- **Method:** `GET`
- **Response:**
  ```json
  { "message": "Hello World" }
  ```

### 2. Greet Endpoint

- **URL:** `/greet/{name}`
- **Method:** `GET`
- **Path Parameter:**
  - `name` (string): The name to greet.
- **Response:**
  ```json
  { "message": "Hello, {name}!" }
  ```
  Example: `/greet/jay` returns `{ "message": "Hello, jay!" }`

---

## How to Run

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the FastAPI server:**
   ```bash
   uvicorn src.main:app --reload
   ```

3. **Access the API docs:**
   Visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) for interactive Swagger UI.

---

## Testing

Automated tests are provided using `pytest` and FastAPI's `TestClient`.

- **Run all tests:**
  ```bash
  pytest
  ```

- **Test coverage:**
  ```bash
  pytest --cov=src
  ```

Tests cover:
- The root endpoint (`/`)
- The greet endpoint (`/greet/{name}`)
- Error handling for missing path parameters

---

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Pytest & pytest-asyncio
- httpx (for async HTTP testing)
- flake8 (optional, for linting)

See `requirements.txt` for exact versions.

---

Happy coding!
