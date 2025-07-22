# Math Utils API - Flask REST API with Tox Testing

A comprehensive Flask-based REST API for mathematical operations, demonstrating advanced testing practices with Tox, comprehensive error handling, and API best practices.

## Project Overview

This project extends the basic math_utils library into a full REST API, showcasing:
- **Flask API Development** with proper error handling
- **Advanced Tox Configuration** with multiple test environments
- **Comprehensive Test Coverage** including API endpoint testing
- **Error Handling Best Practices** for production APIs
- **Code Quality Tools** integration (linting, formatting, coverage)

## Project Structure

```
math_utils_api/
├── app/
│   ├── __init__.py          # Package initialization with exports
│   ├── api.py              # Flask API endpoints with error handling
│   └── calculator.py       # Core calculator functions
├── tests/
│   ├── __init__.py         # Test package initialization
│   ├── test_api.py         # Comprehensive API endpoint tests
│   └── test_calculator.py  # Unit tests for calculator functions
├── pyproject.toml          # Project config with advanced Tox setup
├── requirements.txt        # Runtime dependencies
└── README.md              # This comprehensive guide
```

## API Endpoints

### Core Mathematical Operations

| Endpoint | Method | Description | Example Request | Example Response |
|----------|---------|-------------|----------------|------------------|
| `POST /add` | POST | Addition | `{"a": 5, "b": 3}` | `{"result": 8}` |
| `POST /subtract` | POST | Subtraction | `{"a": 10, "b": 4}` | `{"result": 6}` |
| `POST /multiply` | POST | Multiplication | `{"a": 3, "b": 7}` | `{"result": 21}` |
| `POST /divide` | POST | Division | `{"a": 15, "b": 3}` | `{"result": 5.0}` |

### Health Check Endpoints

| Endpoint | Method | Description | Response |
|----------|---------|-------------|----------|
| `GET /` | GET | Main health check | `{"status": "healthy", "service": "math_utils_api", "version": "0.1.0"}` |
| `GET /health` | GET | Simple health check | `{"status": "ok"}` |

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Quick Start

1. **Navigate to project directory**
   ```bash
   cd math_utils_api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install flask pytest requests
   ```

3. **Install Tox for testing**
   ```bash
   pipx install tox
   # or
   pip install tox
   ```

## Running the Application

### Development Server
```bash
# Set environment variables
export FLASK_APP=app.api
export FLASK_ENV=development

# Run the development server
python -m flask run

# Or run directly
python -c "from app.api import app; app.run(debug=True)"
```

The API will be available at `http://localhost:5000`

### Production Considerations
For production deployment, use a WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn "app.api:app"
```

## Testing

### Run Tests with Pytest
```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html

# Run specific test file
python -m pytest tests/test_api.py -v
```

### Run Tests with Tox (Recommended)
```bash
# Run all test environments
tox

# Run specific environment
tox -e py39-reqslatest

# Run linting only
tox -e lint

# Run coverage report
tox -e coverage

# Format code
tox -e format

# List all available environments
tox -l
```

### Expected Test Output
```
============================== test session starts ===============================
tests/test_api.py::test_add_endpoint PASSED                    [  7%]
tests/test_api.py::test_subtract_endpoint PASSED              [ 14%]
tests/test_api.py::test_multiply_endpoint PASSED              [ 21%]
tests/test_api.py::test_divide_endpoint PASSED                [ 28%]
tests/test_api.py::test_health_check_endpoint PASSED          [ 35%]
tests/test_api.py::test_health_endpoint PASSED                [ 42%]
tests/test_api.py::test_not_found_endpoint PASSED             [ 50%]
tests/test_api.py::test_method_not_allowed PASSED             [ 57%]
tests/test_api.py::test_divide_by_zero_endpoint PASSED        [ 64%]
tests/test_api.py::test_missing_json_data PASSED              [ 71%]
tests/test_api.py::test_missing_parameters PASSED             [ 78%]
tests/test_api.py::test_invalid_parameter_types PASSED        [ 85%]
tests/test_api.py::test_empty_json_data PASSED                [ 92%]
tests/test_api.py::test_null_parameters PASSED                [100%]

================================ 14 passed in 0.05s ===============================
```

## API Usage Examples

### Using curl

#### Basic Operations
```bash
# Addition
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"a": 5, "b": 3}'

# Division
curl -X POST http://localhost:5000/divide \
  -H "Content-Type: application/json" \
  -d '{"a": 15, "b": 3}'

# Health check
curl http://localhost:5000/health
```

#### Error Cases
```bash
# Division by zero
curl -X POST http://localhost:5000/divide \
  -H "Content-Type: application/json" \
  -d '{"a": 10, "b": 0}'
# Returns: {"error": "Cannot divide by zero"}

# Missing parameters
curl -X POST http://localhost:5000/add \
  -H "Content-Type: application/json" \
  -d '{"a": 5}'
# Returns: {"error": "Missing required parameters 'a' and 'b'"}
```

### Using Python requests

```python
import requests
import json

# API base URL
BASE_URL = "http://localhost:5000"

# Addition example
response = requests.post(
    f"{BASE_URL}/add",
    json={"a": 10, "b": 5}
)
print(response.json())  # {'result': 15}

# Error handling example
try:
    response = requests.post(
        f"{BASE_URL}/divide",
        json={"a": 10, "b": 0}
    )
    if response.status_code == 400:
        print(f"Error: {response.json()['error']}")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
```

##  Advanced Tox Configuration

### Multi-Environment Testing
The project tests across multiple Python versions and dependency combinations:

```toml
envlist = py{38,39,310,311}-{reqsmin,reqslatest},lint,coverage
```

- **Python Versions**: 3.8, 3.9, 3.10, 3.11
- **Dependency Variants**:
  - `reqsmin`: Minimum supported versions
  - `reqslatest`: Latest available versions

### Available Tox Environments

| Environment | Purpose | Command |
|-------------|---------|---------|
| `py39-reqslatest` | Test with Python 3.9 + latest deps | `tox -e py39-reqslatest` |
| `lint` | Code quality checks | `tox -e lint` |
| `coverage` | Coverage reporting | `tox -e coverage` |
| `format` | Code formatting | `tox -e format` |

## 🔍 Error Handling

### API Error Responses

The API provides comprehensive error handling with appropriate HTTP status codes:

#### 400 Bad Request
- Missing JSON data
- Missing required parameters
- Invalid parameter types
- Division by zero

#### 404 Not Found
- Invalid endpoint

#### 405 Method Not Allowed
- Wrong HTTP method

#### 500 Internal Server Error
- Unexpected server errors

### Error Response Format
```json
{
  "error": "Descriptive error message"
}
```

## Test Coverage

### Test Categories Covered

#### Unit Tests (`test_calculator.py`)
- ✅ Basic arithmetic operations
- ✅ Edge cases (negative numbers, zero, decimals)
- ✅ Error conditions (division by zero)

#### API Integration Tests (`test_api.py`)
- ✅ **Successful Operations**: All mathematical endpoints
- ✅ **Health Checks**: Root and health endpoints
- ✅ **Error Handling**: Invalid requests, missing data, type errors
- ✅ **HTTP Methods**: Correct status codes and responses
- ✅ **Edge Cases**: Division by zero, null values, empty data

### Coverage Metrics
Run coverage report to see detailed metrics:
```bash
tox -e coverage
# Opens htmlcov/index.html for detailed coverage report
```

## Code Quality

### Linting and Formatting Tools

- **flake8**: Python code linting
- **black**: Code formatting
- **isort**: Import sorting

### Running Quality Checks
```bash
# Check code quality
tox -e lint

# Format code automatically
tox -e format

# Manual formatting
black app/ tests/
isort app/ tests/
flake8 app/ tests/
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: API Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.8, 3.9, '3.10', 3.11]

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install tox
      run: pip install tox
    - name: Run tests
      run: tox
    - name: Run linting
      run: tox -e lint
```

## Key Learning Points

### Flask API Development
1. **Endpoint Structure**: RESTful design principles
2. **Request Validation**: Proper input validation and sanitization
3. **Error Handling**: Comprehensive error responses with appropriate status codes
4. **Testing**: Flask test client usage and API testing patterns

### Advanced Testing Practices
1. **Test Organization**: Separate unit and integration tests
2. **Fixture Usage**: Flask app configuration for testing
3. **Error Case Testing**: Comprehensive error scenario coverage
4. **Parameterized Testing**: Multiple environment configurations

### Production Readiness
1. **Error Handling**: Graceful error responses
2. **Health Checks**: Monitoring and uptime endpoints
3. **Input Validation**: Security and data integrity
4. **Logging**: Structured error reporting

## Development Workflow

### Recommended Development Process
1. **Write Tests First**: Follow TDD principles
2. **Run Tests Locally**: `tox -e py39-reqslatest`
3. **Check Code Quality**: `tox -e lint`
4. **Format Code**: `tox -e format`
5. **Full Test Suite**: `tox`
6. **Coverage Check**: `tox -e coverage`

### Pre-commit Hooks (Optional)
```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: tox-lint
        name: tox lint
        entry: tox -e lint
        language: system
        pass_filenames: false
```

## Next Steps & Extensions

### Immediate Improvements
1. **Add Authentication**: JWT or API key authentication
2. **Rate Limiting**: Prevent API abuse
3. **Request Logging**: Structured logging with request IDs
4. **API Documentation**: OpenAPI/Swagger documentation

### Advanced Features
1. **Database Integration**: Store calculation history
2. **Async Support**: Convert to async Flask or FastAPI
3. **Caching**: Redis caching for common calculations
4. **Monitoring**: Prometheus metrics and health checks

### Learning Extensions
1. **Docker Integration**: Containerized deployment
2. **GraphQL API**: Alternative API design
3. **WebSocket Support**: Real-time calculations
4. **Microservices**: Split into multiple services

##  Additional Resources

### Flask Resources
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask Testing Guide](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [Flask Best Practices](https://flask.palletsprojects.com/en/2.3.x/patterns/)

### API Design
- [RESTful API Design](https://restfulapi.net/)
- [HTTP Status Code Guide](https://httpstatuses.com/)
- [API Testing Best Practices](https://assertible.com/blog/api-testing-best-practices)

### Testing Resources
- [Pytest Flask Plugin](https://pytest-flask.readthedocs.io/)
- [API Testing with Python](https://realpython.com/api-integration-in-python/)

## Troubleshooting

### Common Issues

**1. Import Errors**
```bash
# Ensure you're in the project directory
cd math_utils_api

# Check Python path
export PYTHONPATH=$(pwd):$PYTHONPATH
```

**2. Flask App Not Starting**
```bash
# Set Flask app environment variable
export FLASK_APP=app.api
flask run
```

**3. Test Failures**
```bash
# Run tests with verbose output
pytest tests/ -vv -s

# Run specific failing test
pytest tests/test_api.py::test_add_endpoint -vv
```

**4. Tox Environment Issues**
```bash
# Recreate tox environments
tox -r

# List available environments
tox -l
```

## Contributing

When contributing to this project:
1. **Follow the testing workflow**: Write tests first
2. **Maintain code quality**: Ensure `tox -e lint` passes
3. **Update documentation**: Keep README current
4. **Test thoroughly**: Run full test suite with `tox`

---

*This project demonstrates production-ready Flask API development with comprehensive testing using Tox.* 🚀🧪

**Happy API Development!** 🎉
