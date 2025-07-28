# Math Utils API

This project is a simple REST API built with FastAPI that provides basic arithmetic operations: addition, subtraction, multiplication, and division. It serves as a beginner-friendly example of how to create a well-structured and tested Python application.

The primary goal of this project is to demonstrate:
- Creating a basic API with FastAPI.
- Writing effective unit tests with `pytest`.
- Using `doctest` for simple, example-based testing.
- Best practices for project structure and dependency management.

## Features

- **Four Basic Math Operations**:
  - `POST /add`: Adds two numbers.
  - `POST /subtract`: Subtracts two numbers.
  - `POST /multiply`: Multiplies two numbers.
  - `POST /divide`: Divides two numbers.
- **Input Validation**: Ensures that inputs are valid numbers and handles division-by-zero errors gracefully.
- **Comprehensive Test Suite**: Includes both unit tests and doctests to ensure the application works as expected.

## Project Structure

```
math_utils_api/
├── app/
│   ├── __init__.py       # Makes 'app' a Python package
│   ├── api.py            # Defines the FastAPI endpoints
│   └── calculator.py     # Contains the core business logic (math functions)
├── tests/
│   ├── __init__.py       # Makes 'tests' a Python package
│   ├── test_api.py       # Pytest tests for the API endpoints
│   └── test_calculator.py# Pytest tests for the calculator functions
├── pyproject.toml        # Project metadata and dependencies
└── README.md             # This file
```

## Setup and Installation

To get this project up and running, follow these steps.

### 1. Clone the Repository

If you haven't already, clone the repository to your local machine.

### 2. Create a Virtual Environment

It's highly recommended to use a virtual environment to manage project-specific dependencies.

```sh
# Navigate to the project directory
cd python-beginner/workspace/8_testing/doctest/math_utils_api

# Create a virtual environment
python -m venv .venv

# Activate the virtual environment
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .\.venv\Scripts\activate
```

### 3. Install Dependencies

This project uses `pyproject.toml` to manage dependencies. You can install them using `pip`. The `[test]` option installs both the main dependencies and the testing libraries.

```sh
pip install ".[test]"
```

## Running the Application

To run the API server locally, use `uvicorn`. It will start a development server that automatically reloads when you make changes to the code.

```sh
uvicorn app.api:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can access the interactive API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

## Running Tests

This project uses `pytest` to run both the unit tests and doctests.

To run all tests, simply execute the `pytest` command in the project's root directory:

```sh
pytest -v
```

The `-v` flag provides more verbose output, showing which tests passed. Pytest will automatically discover and run all tests in the `tests/` directory and the doctests within the `app/calculator.py` file.