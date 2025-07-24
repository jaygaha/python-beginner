# Nose2 Testing Tutorial

Nose2 is a testing framework for Python that extends the built-in `unittest` module. It's designed to be simple, flexible, and powerful for writing and running tests in Python projects.

## What is Nose2?

Nose2 is the successor to the original Nose testing framework. It provides:
- Test discovery and execution
- Plugin architecture for extensibility
- Integration with unittest
- Support for test fixtures and parameterized tests
- Detailed test reporting

## Installation

Install Nose2 using pip:

```bash
pip install nose2
```

For development dependencies, you can install it as an optional dependency:

```bash
pip install -e .[test]
```

## Project Structure

```
nose/
├── README.md
├── math_utils/          # Basic unit testing demo
│   ├── README.md
│   ├── pyproject.toml   # Project configuration
│   ├── requirements.txt
│   ├── app/
│   │   ├── __init__.py
│   │   └── calculator.py  # Main module to test
│   └── tests/
│       ├── __init__.py
│       └── test_calculator.py  # Test cases
└── math_utils_api/      # Flask API testing demo
    ├── README.md
    ├── pyproject.toml   # Flask project configuration
    ├── requirements.txt
    ├── app/
    │   ├── __init__.py
    │   ├── calculator.py  # Calculator functions
    │   └── api.py        # Flask REST API
    └── tests/
        ├── __init__.py
        ├── test_calculator.py  # Unit tests
        └── test_api.py    # API endpoint tests
```

## Writing Tests with Nose2

Nose2 uses the standard `unittest` framework. Here are the key concepts:

### 1. Test Discovery

Nose2 automatically discovers tests by looking for:
- Files that start with `test_`
- Classes that inherit from `unittest.TestCase`
- Methods that start with `test_`

### 2. Basic Test Structure

```python
import unittest
from app.calculator import add, subtract, multiply, divide

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
    
    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)
```

### 3. Common Assertions

- `assertEqual(a, b)` - Check if a equals b
- `assertNotEqual(a, b)` - Check if a doesn't equal b
- `assertTrue(x)` - Check if x is True
- `assertFalse(x)` - Check if x is False
- `assertRaises(Exception, func, *args)` - Check if function raises exception
- `assertIn(a, b)` - Check if a is in b
- `assertIsNone(x)` - Check if x is None

### 4. Testing Exceptions

```python
def test_divide_by_zero(self):
    with self.assertRaises(ValueError):
        divide(5, 0)
```

## Running Tests

### Basic Commands

```bash
# Run all tests
nose2

# Run with verbose output
nose2 -v

# Run specific test module
nose2 tests.test_calculator

# Run specific test class
nose2 tests.test_calculator.TestCalculator

# Run specific test method
nose2 tests.test_calculator.TestCalculator.test_add
```

### Configuration Options

Create a `nose2.cfg` file for custom configuration:

```ini
[unittest]
start-dir = tests
code-directories = app

[test-result]
always-on = True
descriptions = True
```

## Test Fixtures

### Setup and Teardown Methods

```python
class TestCalculator(unittest.TestCase):
    def setUp(self):
        """Called before each test method"""
        self.calculator = Calculator()
    
    def tearDown(self):
        """Called after each test method"""
        self.calculator = None
    
    @classmethod
    def setUpClass(cls):
        """Called once before all test methods in the class"""
        pass
    
    @classmethod
    def tearDownClass(cls):
        """Called once after all test methods in the class"""
        pass
```

## Advanced Features

### 1. Parameterized Tests

```python
from nose2.tools import params

class TestMath(unittest.TestCase):
    @params(
        (2, 3, 5),
        (4, 5, 9),
        (-1, 1, 0)
    )
    def test_add_params(self, a, b, expected):
        self.assertEqual(add(a, b), expected)
```

### 2. Skip Tests

```python
import unittest

class TestCalculator(unittest.TestCase):
    @unittest.skip("Skipping this test")
    def test_skip_example(self):
        pass
    
    @unittest.skipIf(sys.version_info < (3, 8), "Requires Python 3.8+")
    def test_conditional_skip(self):
        pass
```

### 3. Test Coverage

Install coverage plugin:

```bash
pip install coverage
```

Run tests with coverage:

```bash
nose2 --with-coverage --coverage-report html
```

## Best Practices

1. **Organize Tests**: Keep tests in a separate `tests/` directory
2. **Descriptive Names**: Use clear, descriptive test method names
3. **One Assertion Per Test**: Focus each test on a single behavior
4. **Use Setup/Teardown**: Clean up resources properly
5. **Test Edge Cases**: Include boundary conditions and error cases
6. **Mock External Dependencies**: Use `unittest.mock` for external services
7. **Keep Tests Fast**: Avoid slow operations in unit tests

## Examples: Testing with Nose2

### Basic Unit Testing Example (`math_utils/`)

The `math_utils/` directory contains a complete example demonstrating:

- Project structure with `pyproject.toml`
- Simple calculator module with basic operations
- Comprehensive test suite covering normal and edge cases
- Exception testing for error conditions
- Package imports and exports

#### Running the Basic Example

```bash
cd math_utils
pip install -e .[test]
nose2 -v
```

Expected output:
```
test_add (tests.test_calculator.TestCalculator) ... ok
test_divide (tests.test_calculator.TestCalculator) ... ok
test_divide_by_zero (tests.test_calculator.TestCalculator) ... ok
test_multiply (tests.test_calculator.TestCalculator) ... ok
test_subtract (tests.test_calculator.TestCalculator) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.001s

OK
```

### Flask API Testing Example (`math_utils_api/`)

The `math_utils_api/` directory demonstrates advanced testing concepts for web APIs:

- Flask REST API with mathematical operations
- API endpoint testing with HTTP requests/responses
- JSON payload validation and error handling
- Integration testing for web services
- Comprehensive error condition testing

Key features:
- **Health Check Endpoints**: `GET /` and `GET /health`
- **Mathematical Operations**: `POST /add`, `/subtract`, `/multiply`, `/divide`
- **Error Handling**: Proper HTTP status codes and JSON error responses
- **Input Validation**: Robust validation of JSON payloads

#### Running the API Testing Example

```bash
cd math_utils_api
pip install -e .[test]
nose2 -v
```

Expected output:
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

#### Testing API Endpoints

The API testing example shows how to test REST endpoints:

```python
class TestApi(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_add_endpoint(self):
        response = self.client.post('/add', json={'a': 2, 'b': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['result'], 5)

    def test_add_invalid_input(self):
        response = self.client.post('/add', json={'a': 'invalid', 'b': 3})
        self.assertEqual(response.status_code, 400)
```

## Integration with CI/CD

Nose2 works well with continuous integration systems:

### GitHub Actions Example

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    - name: Install dependencies
      run: |
        pip install -e .[test]
    - name: Run tests
      run: nose2 -v
```

## Comparison with Other Testing Frameworks

| Feature | Nose2 | pytest | unittest |
|---------|-------|--------|----------|
| Test Discovery | ✓ | ✓ | Limited |
| Fixtures | ✓ | ✓✓ | Basic |
| Parameterization | ✓ | ✓✓ | - |
| Plugin System | ✓ | ✓✓ | - |
| Learning Curve | Easy | Medium | Easy |
| Compatibility | unittest | Wide | Built-in |

## Resources

- [Nose2 Documentation](https://docs.nose2.io/)
- [Python unittest Documentation](https://docs.python.org/3/library/unittest.html)
- [Test-Driven Development Guide](https://testdriven.io/test-driven-development/)

## Next Steps

1. **Start with Basic Testing**: Explore the `math_utils/` example package
2. **Progress to API Testing**: Try the `math_utils_api/` Flask example
3. **Write Your Own Tests**: Create test cases for your own projects
4. **Experiment with Advanced Features**: Try fixtures and parameterized tests
5. **Set Up Test Coverage**: Use coverage reporting to improve test quality
6. **Integrate with CI/CD**: Add testing to your development workflow
7. **Explore Web Testing**: Learn more about testing REST APIs and web services

## Choosing Your Starting Point

- **New to Testing?** Start with the `math_utils/` basic example
- **Building Web APIs?** Jump to the `math_utils_api/` Flask example  
- **Want Both?** Work through both examples in order

Each example includes comprehensive documentation and step-by-step instructions to help you learn Nose2 testing effectively.