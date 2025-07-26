# Python Testing with pytest

This directory contains examples and exercises for learning Python testing using the pytest framework and unittest module.

## Table of Contents

- [Overview](#overview)
- [Testing Fundamentals](#testing-fundamentals)
- [pytest vs unittest](#pytest-vs-unittest)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Running Tests](#running-tests)
- [Testing Best Practices](#testing-best-practices)
- [Common Testing Patterns](#common-testing-patterns)
- [Resources](#resources)

## Overview

Testing is a crucial part of software development that helps ensure your code works correctly and continues to work as you make changes. This project demonstrates various testing concepts using Python's built-in `unittest` module and the popular `pytest` framework.

## Testing Fundamentals

### Why Test?

- **Catch bugs early**: Find issues before they reach production
- **Refactoring confidence**: Make changes without fear of breaking existing functionality
- **Documentation**: Tests serve as living documentation of how your code should behave
- **Design improvement**: Writing tests often leads to better code design

### Types of Tests

1. **Unit Tests**: Test individual functions or methods in isolation
2. **Integration Tests**: Test how different parts of your application work together
3. **Functional Tests**: Test complete features from the user's perspective

## pytest vs unittest

### unittest (Built-in)
- Part of Python's standard library
- Class-based approach
- More verbose syntax
- Built-in assertions like `assertEqual()`, `assertTrue()`

### pytest (Third-party)
- More concise and readable
- Function-based approach (though classes are supported)
- Simple `assert` statements
- Powerful fixtures and plugins
- Better error reporting

## Project Structure

```
pytest/
├── README.md                 # This file
├── math_utils/              # Basic calculator library example
│   ├── README.md           # Math utils documentation
│   ├── pyproject.toml      # Project configuration
│   ├── requirements.txt    # Dependencies
│   ├── app/               # Main application code
│   │   ├── __init__.py
│   │   └── calculator.py   # Calculator functions
│   └── tests/             # Test files
│       ├── __init__.py
│       └── test_calculator.py  # Calculator tests (unittest)
└── math_utils_api/         # FastAPI web service example
    ├── README.md           # API documentation
    ├── pyproject.toml      # Project configuration
    ├── pytest.ini         # Pytest configuration
    ├── requirements.txt    # Dependencies
    ├── app/               # FastAPI application
    │   ├── __init__.py
    │   ├── api.py          # FastAPI endpoints
    │   └── calculator.py   # Core calculation functions
    └── tests/             # Test suite
        ├── __init__.py
        ├── test_api.py     # API endpoint tests (pytest)
        └── test_calculator.py  # Calculator tests (unittest)
```

## Getting Started

### Prerequisites

Make sure you have Python installed. You can check by running:
```bash
python --version
```

### Installing pytest

```bash
# Install pytest
pip install pytest

# Or install with additional plugins
pip install pytest pytest-cov pytest-mock
```

### Basic Test Example

Here's a simple example of a test function:

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```

## Running Tests

### Using unittest

```bash
# Run all tests in a module
python -m unittest test_calculator.py

# Run a specific test class
python -m unittest test_calculator.TestCalculator

# Run a specific test method
python -m unittest test_calculator.TestCalculator.test_add

# Run with verbose output
python -m unittest -v test_calculator.py
```

### Using pytest

```bash
# Run all tests in current directory
pytest

# Run tests in a specific file
pytest test_calculator.py

# Run a specific test function
pytest test_calculator.py::test_add

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app

# Run and stop at first failure
pytest -x
```

## Testing Best Practices

### 1. Test Naming
- Use descriptive names: `test_add_positive_numbers()`
- Follow the pattern: `test_<function>_<scenario>_<expected_result>()`

### 2. Test Structure (AAA Pattern)
```python
def test_divide_by_zero_raises_error():
    # Arrange
    a, b = 10, 0
    
    # Act & Assert
    with pytest.raises(ValueError):
        divide(a, b)
```

### 3. Test Independence
- Each test should be independent
- Don't rely on the order of test execution
- Use setup and teardown methods when needed

### 4. Test One Thing at a Time
```python
# Good - tests one specific behavior
def test_add_positive_numbers():
    assert add(2, 3) == 5

def test_add_negative_numbers():
    assert add(-2, -3) == -5

# Avoid - tests multiple behaviors
def test_add_all_cases():
    assert add(2, 3) == 5
    assert add(-2, -3) == -5
    assert add(0, 0) == 0
```

### 5. Use Meaningful Assertions
```python
# Good - specific assertion
assert len(result) == 3

# Less clear - generic assertion
assert result
```

## Common Testing Patterns

### Testing Exceptions

```python
# unittest style
def test_divide_by_zero(self):
    with self.assertRaises(ValueError):
        divide(6, 0)

# pytest style
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(6, 0)
```

### Parametrized Tests (pytest)

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
])
def test_add(a, b, expected):
    assert add(a, b) == expected
```

### Fixtures (pytest)

```python
@pytest.fixture
def calculator():
    return Calculator()

def test_add_with_fixture(calculator):
    result = calculator.add(2, 3)
    assert result == 5
```

### Mocking

```python
from unittest.mock import patch

@patch('requests.get')
def test_api_call(mock_get):
    mock_get.return_value.json.return_value = {'result': 'success'}
    # Test code that uses requests.get
```

## Example Projects

### Math Utils Library

The `math_utils` directory contains a basic calculator library demonstrating:

- Basic calculator functions (add, subtract, multiply, divide)
- Comprehensive test coverage using unittest
- Project structure following Python best practices
- Error handling and edge case testing

**Key Features Tested:**
1. **Basic Operations**: Addition, subtraction, multiplication, division
2. **Edge Cases**: Zero values, negative numbers
3. **Error Handling**: Division by zero raises appropriate exception
4. **Multiple Test Cases**: Each function tested with various inputs

### Math Utils API (FastAPI)

The `math_utils_api` directory contains a production-ready web API demonstrating:

- **FastAPI Implementation**: RESTful API with automatic documentation
- **Advanced Testing**: 65+ test cases using pytest framework
- **Input Validation**: Pydantic models with custom validators
- **Error Handling**: Comprehensive HTTP error responses
- **API Testing**: HTTP endpoint testing with TestClient
- **Production Features**: Logging, configuration, and deployment ready

**Key Features Demonstrated:**
1. **RESTful Endpoints**: POST endpoints for mathematical operations
2. **Input Validation**: Automatic request/response validation
3. **Error Handling**: Proper HTTP status codes and error messages
4. **Interactive Documentation**: Auto-generated Swagger UI and ReDoc
5. **Comprehensive Testing**: API integration tests, edge cases, concurrent testing
6. **Type Safety**: Full type hints with Pydantic models

**API Endpoints:**
- `POST /add` - Addition operation
- `POST /subtract` - Subtraction operation
- `POST /multiply` - Multiplication operation
- `POST /divide` - Division operation (with zero-division protection)

**Quick Start:**
```bash
cd math_utils_api
pip install -r requirements.txt
uvicorn app.api:app --reload
# Visit http://localhost:8000/docs for interactive documentation
```

## Resources

### Documentation
- [pytest Documentation](https://docs.pytest.org/)
- [unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Python Testing 101](https://realpython.com/python-testing/)

### Best Practices
- [Effective Python Testing With Pytest](https://realpython.com/pytest-python-testing/)
- [Testing Best Practices](https://docs.python-guide.org/writing/tests/)

### Tools and Extensions
- [pytest-cov](https://pytest-cov.readthedocs.io/) - Coverage reporting
- [pytest-mock](https://pytest-mock.readthedocs.io/) - Mocking utilities
- [pytest-xdist](https://pytest-xdist.readthedocs.io/) - Parallel testing

## API Testing with FastAPI

The `math_utils_api` project demonstrates advanced testing concepts for web APIs:

### FastAPI Testing Features

```python
from fastapi.testclient import TestClient
from app.api import app

@pytest.fixture(scope="class")
def client():
    return TestClient(app)

def test_api_endpoint(client):
    response = client.post("/add", json={"a": 2, "b": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 5}
```

### Key Testing Concepts Covered

1. **HTTP Testing**: Using TestClient for endpoint testing
2. **Input Validation Testing**: Pydantic model validation
3. **Error Response Testing**: HTTP status codes and error messages
4. **Parametrized API Tests**: Testing multiple scenarios efficiently
5. **Concurrent Testing**: Verifying API reliability under load
6. **Integration Testing**: End-to-end API workflow testing

### Advanced pytest Features

- **Fixtures**: Reusable test setup and data
- **Parametrization**: Data-driven testing
- **Markers**: Categorizing and filtering tests
- **Coverage**: Code coverage reporting
- **Concurrent Testing**: Multi-threaded test scenarios

## Next Steps

1. **Start with math_utils**: Learn basic testing concepts
2. **Progress to math_utils_api**: Explore web API testing
3. **Experiment with pytest fixtures**: Create reusable test components
4. **Try parametrized tests**: Test multiple scenarios efficiently
5. **Learn about mocking**: Test external dependencies
6. **Practice TDD**: Write tests before implementation
7. **Explore FastAPI testing**: HTTP endpoint and integration testing

### Learning Path

**Beginner** → `math_utils` (unittest basics)
**Intermediate** → `math_utils_api` (pytest + FastAPI)
**Advanced** → Custom fixtures, mocking, CI/CD integration

Remember: Good tests are as important as good code. They give you confidence to refactor, extend, and maintain your software over time.