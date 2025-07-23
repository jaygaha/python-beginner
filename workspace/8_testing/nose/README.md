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
└── math_utils/          # Demo package
    ├── README.md
    ├── pyproject.toml   # Project configuration
    ├── requirements.txt
    ├── app/
    │   ├── __init__.py
    │   └── calculator.py  # Main module to test
    └── tests/
        ├── __init__.py
        └── test_calculator.py  # Test cases
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

## Example: Testing the Math Utils Package

The `math_utils/` directory contains a complete example demonstrating:

- Project structure with `pyproject.toml`
- Simple calculator module with basic operations
- Comprehensive test suite covering normal and edge cases
- Exception testing for error conditions
- Package imports and exports

### Running the Example

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

1. Explore the `math_utils/` example package
2. Try writing your own test cases
3. Experiment with fixtures and parameterized tests
4. Set up test coverage reporting
5. Integrate tests into your development workflow