# Math Utils - Tox Testing Learning Project

A simple Python mathematics utility library created to demonstrate and learn **Tox** testing workflows. This project showcases how to set up automated testing across multiple Python environments using Tox.

## Learning Objectives

This project was created to understand:
- How to configure and use **Tox** for automated testing
- Setting up testing environments with `pyproject.toml`
- Writing comprehensive test suites with **pytest**
- Handling edge cases and error conditions in code
- Creating proper Python package structure

## Project Structure

```
math_utils/
├── app/
│   ├── __init__.py          # Package initialization
│   └── calculator.py        # Core calculator functions
├── tests/
│   ├── __init__.py          # Test package initialization
│   └── test_calculator.py   # Test suite for calculator functions
├── pyproject.toml           # Project configuration and Tox settings
├── requirements.txt         # Project dependencies
└── README.md               # This file
```

## Features

The calculator module provides four basic mathematical operations:

### Functions Available:
- `add(a, b)` - Addition of two numbers
- `subtract(a, b)` - Subtraction of two numbers
- `multiply(a, b)` - Multiplication of two numbers
- `divide(a, b)` - Division of two numbers (with zero-division protection)

### Error Handling:
- **Division by Zero**: Raises `ValueError` with descriptive message
- **Input Validation**: Functions work with integers and floats

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Quick Start

1. **Clone or navigate to the project directory**
   ```bash
   cd math_utils
   ```

2. **Install Tox** (recommended via pipx for isolation)
   ```bash
   # Using pipx (recommended)
   python -m pip install pipx
   pipx install tox

   # Or using pip directly
   pip install tox
   ```

3. **Verify Tox installation**
   ```bash
   tox --version
   ```

## Running Tests

### Using Pytest Directly
```bash
# Run all tests with verbose output
python -m pytest tests/ -v

# Run tests with coverage report
python -m pytest tests/ --cov=app
```

### Using Tox (Recommended)
```bash
# Run tests in default environment
tox

# Run tests in specific Python version
tox -e py

# List available environments
tox -l
```

### Expected Test Output
```
============================== test session starts ===============================
tests/test_calculator.py::test_add PASSED                  [ 20%]
tests/test_calculator.py::test_subtract PASSED             [ 40%]
tests/test_calculator.py::test_multiply PASSED             [ 60%]
tests/test_calculator.py::test_divide PASSED               [ 80%]
tests/test_calculator.py::test_divide_by_zero PASSED       [100%]

=============================== 5 passed in 0.02s ================================
```

## Usage Examples

### Basic Usage
```python
from app.calculator import add, subtract, multiply, divide

# Basic operations
result = add(5, 3)        # Returns: 8
result = subtract(10, 4)  # Returns: 6
result = multiply(3, 7)   # Returns: 21
result = divide(15, 3)    # Returns: 5.0

# Error handling example
try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Error: {e}")  # Prints: Error: Cannot divide by zero
```

### Import from Package
```python
from app import add, subtract, multiply, divide

# All functions are available through the package
result = add(1, 2)
```

## Configuration Details

### Tox Configuration (`pyproject.toml`)
```toml
[tool.tox]
legacy_tox_ini = """
[tox]
envlist = py37,py38,py39,py310
isolated_build = true

[testenv]
deps = pytest>=7.0.0
commands = pytest tests/
"""
```

### Project Metadata
- **Name**: math_utils
- **Version**: 0.1.0
- **Author**: Jay Gaha
- **Dependencies**: pytest (for testing)

## Test Coverage

The test suite covers:
- ✅ **Basic Operations**: All four mathematical operations
- ✅ **Edge Cases**: Negative numbers, zero values, decimal numbers
- ✅ **Error Conditions**: Division by zero handling
- ✅ **Exception Testing**: Proper error message validation

### Test Cases:
1. **Addition Tests**: Positive numbers, negative numbers, zero
2. **Subtraction Tests**: Various number combinations
3. **Multiplication Tests**: Including negative numbers
4. **Division Tests**: Normal division, decimal results, zero dividend
5. **Error Tests**: Division by zero exception handling

## Key Learning Points

### Tox Benefits Demonstrated:
1. **Environment Isolation**: Each test runs in a clean virtual environment
2. **Reproducible Testing**: Same results across different machines
3. **Multi-version Testing**: Easy testing across Python versions
4. **CI/CD Ready**: Perfect for automated pipelines

### Testing Best Practices:
1. **Comprehensive Coverage**: Test normal cases, edge cases, and error conditions
2. **Clear Test Names**: Descriptive function names for easy understanding
3. **Proper Assertions**: Using pytest's powerful assertion features
4. **Error Testing**: Validating exception handling with `pytest.raises()`

## Next Steps

To extend your learning:
1. **Add More Test Environments**: Configure different Python versions
2. **Code Coverage**: Add coverage reporting with `pytest-cov`
3. **Linting Integration**: Add flake8 or black formatting checks
4. **Documentation Testing**: Use doctest for inline documentation tests
5. **Performance Testing**: Add benchmarking for mathematical operations

## Additional Resources

- [Tox Official Documentation](https://tox.readthedocs.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Python Testing Best Practices](https://realpython.com/python-testing/)
- [PyProject.toml Specification](https://peps.python.org/pep-0621/)

## Notes

This is a learning project focused on understanding Tox workflow and testing practices. The mathematical operations are intentionally simple to keep focus on the testing methodology rather than complex algorithms.

---

*Created as part of Python testing fundamentals learning path* 🐍
