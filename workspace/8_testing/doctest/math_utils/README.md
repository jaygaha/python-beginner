# Math Utils - A Simple Calculator Library with Doctests

A Python package demonstrating the use of doctests for testing mathematical operations.

## Overview

This package provides basic mathematical operations (add, subtract, multiply, divide) with comprehensive doctests embedded in the function docstrings.

## Project Structure

```
math_utils/
├── app/
│   ├── __init__.py          # Package initialization
│   └── calculator.py        # Main calculator functions with doctests
├── tests/
│   ├── __init__.py          # Test package initialization
│   └── test_calculator.py   # Unit tests + doctest integration
├── run_doctests.py          # Standalone doctest runner
├── pyproject.toml          # Project configuration
└── README.md               # This file
```

## Installation

No external dependencies are required. This package uses only Python standard library modules.

## Usage

### Basic Usage

```python
from app.calculator import add, subtract, multiply, divide

# Basic operations
result = add(2, 3)        # Returns 5
result = subtract(5, 3)   # Returns 2
result = multiply(2, 4)   # Returns 8
result = divide(10, 2)    # Returns 5.0

# Error handling
try:
    result = divide(10, 0)
except ValueError as e:
    print(e)  # "Cannot divide by zero"
```

## Testing

This project demonstrates three different ways to run doctests:

### 1. Using Python's Built-in Doctest Module

Run doctests directly on the calculator module:

```bash
python -m doctest app/calculator.py -v
```

### 2. Using the Custom Doctest Runner

Run all doctests with detailed output:

```bash
python run_doctests.py
```

Run doctests for a specific function:

```bash
python run_doctests.py add
python run_doctests.py divide
```

### 3. Using Unittest with Integrated Doctests

Run both unit tests and doctests together:

```bash
python -m unittest tests.test_calculator -v
```

Or using pytest:

```bash
python -m pytest tests/test_calculator.py -v
```

## Doctest Examples

Each function in the calculator module includes doctests in its docstring:

### Addition Function
```python
def add(a, b):
    """
    Add two numbers.

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b
```

### Division with Error Handling
```python
def divide(a, b):
    """
    Divide a by b, raising ValueError if b is zero.

    >>> divide(6, 3)
    2.0
    >>> divide(5, 2)
    2.5
    >>> divide(10, 0)
    Traceback (most recent call last):
        ...
    ValueError: Cannot divide by zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## Test Coverage

The project includes:
- **9 doctests** embedded in function docstrings
- **5 unit tests** for comprehensive function testing
- **Error handling tests** for edge cases

### Current Test Results
- All 9 doctests pass
- All 5 unit tests pass
- Exception handling works correctly

## Key Features Demonstrated

1. **Doctests as Documentation**: Function docstrings serve as both documentation and tests
2. **Exception Testing**: Shows how to test exception scenarios in doctests
3. **Integration**: Demonstrates combining doctests with traditional unit tests
4. **Multiple Test Runners**: Shows different ways to execute the same tests

## Benefits of Doctests

- **Documentation**: Tests serve as executable examples
- **Simplicity**: Easy to write and maintain
- **Integration**: Can be combined with other testing frameworks
- **Immediate Feedback**: Tests are visible right in the code

## Common Doctest Patterns

### Testing Return Values
```python
>>> add(2, 3)
5
```

### Testing Exceptions
```python
>>> divide(10, 0)
Traceback (most recent call last):
    ...
ValueError: Cannot divide by zero
```

### Testing Multiple Cases
```python
>>> multiply(2, 3)
6
>>> multiply(-2, 3)
-6
```

## Running All Tests

To run the complete test suite:

```bash
# Run doctests only
python run_doctests.py

# Run unit tests only
python -m unittest tests.test_calculator

# Run both doctests and unit tests
python -m unittest tests.test_calculator -v
```

## Contributing

When adding new functions:
1. Include comprehensive doctests in the docstring
2. Add corresponding unit tests in `tests/test_calculator.py`
3. Update this README with new examples

## License

This project is for educational purposes demonstrating Python doctest usage.
