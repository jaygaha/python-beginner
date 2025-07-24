# Math Utils API - Flask REST API with Nose2 Testing

This package demonstrates testing a Flask REST API using Nose2. It extends the basic `math_utils` example by providing HTTP endpoints for mathematical operations and comprehensive API testing.

## Overview

The `math_utils_api` package demonstrates:
- Flask REST API development
- API endpoint testing with Nose2
- HTTP request/response testing
- Error handling and validation testing
- JSON payload testing
- Integration testing for web services

## Package Structure

```
math_utils_api/
├── README.md              # This file
├── pyproject.toml         # Package configuration with Flask dependencies
├── requirements.txt       # Dependencies including Flask
├── app/                   # Main application code
│   ├── __init__.py       # Package exports
│   ├── calculator.py     # Calculator functions (same as basic example)
│   └── api.py           # Flask API endpoints
└── tests/                # Test suite
    ├── __init__.py       # Test package
    ├── test_calculator.py # Unit tests for calculator functions
    └── test_api.py       # API endpoint tests
```

## Features

### API Endpoints

The Flask application provides the following REST endpoints:

#### Health Check Endpoints
- `GET /` - Primary health check with service information
- `GET /health` - Simple health status

#### Mathematical Operation Endpoints
- `POST /add` - Add two numbers
- `POST /subtract` - Subtract two numbers
- `POST /multiply` - Multiply two numbers
- `POST /divide` - Divide two numbers (with zero division protection)

### Request Format

All mathematical operation endpoints expect JSON payloads:

```json
{
    "a": 10,
    "b": 5
}
```

### Response Format

Successful responses return:

```json
{
    "result": 15
}
```

Error responses return:

```json
{
    "error": "Error description"
}
```

## Installation

### Option 1: Install in Development Mode
```bash
cd math_utils_api
pip install -e .[test]
```

### Option 2: Install Dependencies Manually
```bash
cd math_utils_api
pip install -r requirements.txt
```

## Usage

### Running the API Server

```bash
# Set Flask app
export FLASK_APP=app.api:app
export FLASK_ENV=development

# Run the server
flask run
```

Or programmatically:

```python
from app.api import app

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
```

### Making API Requests

#### Using curl

```bash
# Health check
curl http://localhost:5000/

# Add two numbers
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 5}'

# Subtract
curl -X POST http://localhost:5000/subtract \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 3}'

# Multiply
curl -X POST http://localhost:5000/multiply \
  -H "Content-Type: application/json" \
  -d '{"a": 4, "b": 7}'

# Divide
curl -X POST http://localhost:5000/divide \
  -H "Content-Type: application/json" \
  -d '{"a": 20, "b": 4}'
```

#### Using Python requests

```python
import requests
import json

base_url = "http://localhost:5000"

# Health check
response = requests.get(f"{base_url}/")
print(response.json())

# Mathematical operations
data = {"a": 15, "b": 3}

# Addition
response = requests.post(f"{base_url}/add", json=data)
print(f"15 + 3 = {response.json()['result']}")

# Division
response = requests.post(f"{base_url}/divide", json=data)
print(f"15 / 3 = {response.json()['result']}")
```

## Testing

### Running Tests

```bash
# Run all tests (unit + API tests)
nose2 -v

# Run only unit tests
nose2 -v tests.test_calculator

# Run only API tests
nose2 -v tests.test_api

# Run specific test method
nose2 -v tests.test_api.TestApi.test_add_endpoint
```

### Expected Test Output

```
test_add (tests.test_calculator.TestCalculator) ... ok
test_divide (tests.test_calculator.TestCalculator) ... ok
test_divide_by_zero (tests.test_calculator.TestCalculator) ... ok
test_multiply (tests.test_calculator.TestCalculator) ... ok
test_subtract (tests.test_calculator.TestCalculator) ... ok
test_add_endpoint (tests.test_api.TestApi) ... ok
test_add_invalid_input (tests.test_api.TestApi) ... ok
test_divide_by_zero (tests.test_api.TestApi) ... ok
test_divide_endpoint (tests.test_api.TestApi) ... ok
test_divide_invalid_input (tests.test_api.TestApi) ... ok
test_multiply_endpoint (tests.test_api.TestApi) ... ok
test_multiply_invalid_input (tests.test_api.TestApi) ... ok
test_subtract_endpoint (tests.test_api.TestApi) ... ok

----------------------------------------------------------------------
Ran 13 tests in 0.045s

OK
```

## API Testing Details

### Test Categories

The API test suite covers several important areas:

#### 1. Endpoint Functionality Tests
- Verify each endpoint returns correct mathematical results
- Test with various numeric inputs (positive, negative, decimals)
- Validate JSON response format

#### 2. Input Validation Tests
- Test missing JSON payload
- Test missing required parameters ('a' and 'b')
- Test non-numeric input values
- Test invalid JSON format

#### 3. Error Handling Tests
- Division by zero error handling
- HTTP error codes (400 for bad requests, 500 for server errors)
- Error message format and content

#### 4. HTTP Method Tests
- Verify correct HTTP methods are supported
- Test method not allowed responses (405)

### Test Structure Example

```python
class TestApi(unittest.TestCase):
    def setUp(self):
        """Set up test client before each test"""
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_add_endpoint(self):
        """Test addition endpoint with valid input"""
        response = self.client.post('/add', json={'a': 2, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 5)

    def test_add_invalid_input(self):
        """Test addition endpoint with invalid input"""
        response = self.client.post('/add', json={'a': 'invalid', 'b': 3})
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json)
```

## Error Handling

The API implements comprehensive error handling:

### Client Errors (4xx)

- **400 Bad Request**: Invalid JSON, missing parameters, non-numeric values
- **404 Not Found**: Non-existent endpoints
- **405 Method Not Allowed**: Wrong HTTP method

### Server Errors (5xx)

- **500 Internal Server Error**: Unexpected server-side errors

### Error Response Examples

```json
// Missing parameters
{
    "error": "Missing required parameters 'a' and 'b'"
}

// Non-numeric input
{
    "error": "Parameters 'a' and 'b' must be numeric"
}

// Division by zero
{
    "error": "Cannot divide by zero"
}

// No JSON data
{
    "error": "No JSON data provided"
}
```

## Advanced Testing Features

### Test Fixtures

The API tests use Flask's test client:

```python
def setUp(self):
    """Configure Flask app for testing"""
    app.config['TESTING'] = True
    self.client = app.test_client()
```

### Parameterized Testing

You can extend tests with parameterized inputs:

```python
from nose2.tools import params

@params(
    (2, 3, 5),
    (-1, 1, 0),
    (10.5, 2.5, 13.0)
)
def test_add_multiple(self, a, b, expected):
    response = self.client.post('/add', json={'a': a, 'b': b})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['result'], expected)
```

## Integration Testing

### Database Integration (Future Extension)

For apps with databases, you might add:

```python
def setUp(self):
    app.config['TESTING'] = True
    app.config['DATABASE_URL'] = 'sqlite:///:memory:'
    self.client = app.test_client()
    # Initialize test database
```

### External Service Mocking

Mock external services in tests:

```python
from unittest.mock import patch

@patch('app.api.external_service_call')
def test_with_mocked_service(self, mock_service):
    mock_service.return_value = {'status': 'success'}
    response = self.client.post('/endpoint', json={'data': 'test'})
    self.assertEqual(response.status_code, 200)
```

## Performance Testing

Add performance assertions to your tests:

```python
import time

def test_response_time(self):
    start_time = time.time()
    response = self.client.post('/add', json={'a': 1, 'b': 2})
    end_time = time.time()
    
    self.assertEqual(response.status_code, 200)
    self.assertLess(end_time - start_time, 0.1)  # Should respond in <100ms
```

## Development Workflow

### 1. Test-Driven Development (TDD)

1. **Write failing test**: Create test for new endpoint
2. **Implement endpoint**: Add minimal code to make test pass
3. **Refactor**: Improve code while keeping tests green
4. **Repeat**: Continue for each new feature

### 2. Continuous Testing

```bash
# Run tests on file changes (requires entr or similar)
find . -name "*.py" | entr -r nose2 -v
```

### 3. Pre-commit Testing

Add to `.git/hooks/pre-commit`:

```bash
#!/bin/sh
nose2 -v
if [ $? -ne 0 ]; then
    echo "Tests failed. Commit aborted."
    exit 1
fi
```

## Configuration Management

### Environment-specific Configs

```python
# app/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')
    
class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')  # Must be set in production
```

## Security Testing

### Input Sanitization Tests

```python
def test_sql_injection_attempt(self):
    """Test that SQL injection attempts are handled safely"""
    malicious_input = "'; DROP TABLE users; --"
    response = self.client.post('/add', json={'a': malicious_input, 'b': 2})
    self.assertEqual(response.status_code, 400)
```

### Cross-Site Scripting (XSS) Prevention

```python
def test_xss_attempt(self):
    """Test that XSS attempts are handled safely"""
    xss_input = "<script>alert('xss')</script>"
    response = self.client.post('/add', json={'a': xss_input, 'b': 2})
    self.assertEqual(response.status_code, 400)
```

## Deployment Testing

### Health Check Testing

```python
def test_health_endpoint(self):
    """Test health check endpoint for monitoring"""
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
    data = response.json
    self.assertEqual(data['status'], 'healthy')
    self.assertEqual(data['service'], 'math_utils_api')
```

## Learning Objectives

This API testing demonstration teaches:

1. **Flask Testing**: Using Flask's test client for API testing
2. **HTTP Testing**: Testing different HTTP methods and status codes
3. **JSON Handling**: Testing JSON request/response cycles
4. **Error Testing**: Comprehensive error condition testing
5. **Integration Testing**: Testing complete request/response flows
6. **Validation Testing**: Testing input validation and sanitization

## Best Practices Demonstrated

1. **Separation of Concerns**: Business logic in `calculator.py`, API logic in `api.py`
2. **Comprehensive Testing**: Both unit tests and integration tests
3. **Error Handling**: Proper HTTP status codes and error messages
4. **Input Validation**: Robust validation of JSON inputs
5. **Test Organization**: Clear test structure and descriptive test names
6. **Documentation**: Comprehensive API documentation and examples

## Common API Testing Patterns

### Testing JSON APIs

```python
def test_json_response_structure(self):
    """Test that API returns expected JSON structure"""
    response = self.client.post('/add', json={'a': 1, 'b': 2})
    data = response.json
    self.assertIn('result', data)
    self.assertIsInstance(data['result'], (int, float))
```

### Testing Content Types

```python
def test_content_type_json(self):
    """Test that API returns JSON content type"""
    response = self.client.post('/add', json={'a': 1, 'b': 2})
    self.assertEqual(response.content_type, 'application/json')
```

### Testing Edge Cases

```python
def test_large_numbers(self):
    """Test API with very large numbers"""
    large_num = 10**10
    response = self.client.post('/add', json={'a': large_num, 'b': 1})
    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.json['result'], large_num + 1)
```

## Extending the Example

Try these exercises:

1. **Add Authentication**: Implement API key authentication and test it
2. **Add Rate Limiting**: Implement and test rate limiting
3. **Add Logging**: Add request logging and test log output
4. **Add Caching**: Implement response caching and test cache behavior
5. **Add Database**: Add persistent storage and test CRUD operations
6. **Add Pagination**: Implement pagination for list endpoints
7. **Add Versioning**: Implement API versioning (v1, v2) and test both versions

## Troubleshooting

### Common Issues

**Flask Import Errors**:
```bash
# Make sure Flask is installed
pip install flask

# Check Flask app is properly configured
export FLASK_APP=app.api:app
```

**Test Client Issues**:
```bash
# Ensure you're using Flask's test client correctly
app.config['TESTING'] = True
client = app.test_client()
```

**JSON Response Issues**:
```bash
# Check response content type
print(response.content_type)
print(response.data)  # Raw response data
```

### Debugging Tests

```python
def test_debug_response(self):
    """Debug failing test by examining response"""
    response = self.client.post('/add', json={'a': 1, 'b': 2})
    print(f"Status: {response.status_code}")
    print(f"Data: {response.data}")
    print(f"JSON: {response.json}")
    # Add your assertions here
```

## Next Steps

After exploring this API testing example:

1. Run the Flask server and test endpoints manually
2. Study the test structure and assertion patterns
3. Add new endpoints and corresponding tests
4. Practice error handling and validation testing
5. Explore Flask testing documentation
6. Try building a more complex API with authentication
7. Implement continuous integration with GitHub Actions

This example provides a solid foundation for testing REST APIs with Nose2 and Flask, demonstrating industry-standard patterns for API development and testing.