# Math Utils - Nose2 Testing Demonstration

This package demonstrates testing Python code using Nose2. It contains a simple calculator module with basic mathematical operations and comprehensive test cases.

## Overview

The `math_utils` package is a simple demonstration of:
- Python package structure
- Basic mathematical functions
- Unit testing with Nose2
- Exception handling and testing
- Package configuration with `pyproject.toml`

## Package Structure

```
math_utils/
├── README.md           # This file
├── pyproject.toml      # Package configuration
├── requirements.txt    # Dependencies
├── app/               # Main application code
│   ├── __init__.py    # Package exports
│   └── calculator.py  # Calculator functions
└── tests/             # Test suite
    ├── __init__.py    # Test package
    └── test_calculator.py  # Calculator tests
```

## Features

The calculator module provides four basic operations:
- **Addition**: Add two numbers
- **Subtraction**: Subtract two numbers
- **Multiplication**: Multiply two numbers
- **Division**: Divide two numbers (with zero division protection)

## Installation

### Option 1: Install in Development Mode
```bash
cd math_utils
pip install -e .[test]
```

### Option 2: Install Dependencies Manually
```bash
cd math_utils
pip install -r requirements.txt
```

## Usage

### Using the Calculator Functions

```python
from app.calculator import add, subtract, multiply, divide

# Basic operations
result = add(5, 3)        # Returns: 8
result = subtract(10, 4)  # Returns: 6
result = multiply(3, 7)   # Returns: 21
result = divide(15, 3)    # Returns: 5.0

# Error handling
try:
    result = divide(10, 0)  # Raises ValueError
except ValueError as e:
    print(f"Error: {e}")    # Output: Error: Cannot divide by zero
```

### Using Package Imports

```python
from app import add, subtract, multiply, divide

# All functions are available through the package
total = add(multiply(3, 4), subtract(10, 5))  # Result: 17
```

## Running Tests

### Basic Test Execution

```bash
# Run all tests
nose2

# Run with verbose output
nose2 -v

# Run from project root
nose2 -v tests
```

### Expected Test Output

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

### Running Specific Tests

```bash
# Run specific test module
nose2 tests.test_calculator

# Run specific test class
nose2 tests.test_calculator.TestCalculator

# Run specific test method
nose2 tests.test_calculator.TestCalculator.test_add
```

## Test Coverage

The test suite covers:

### Normal Operations
- Addition with positive and negative numbers
- Subtraction with various combinations
- Multiplication including negative results
- Division with whole and fractional results

### Edge Cases
- Zero division error handling
- Negative number operations
- Floating-point results

### Test Methods

| Test Method | Description |
|------------|-------------|
| `test_add()` | Tests addition with positive, negative, and zero |
| `test_subtract()` | Tests subtraction with various number combinations |
| `test_multiply()` | Tests multiplication including negative results |
| `test_divide()` | Tests division with whole and fractional results |
| `test_divide_by_zero()` | Tests proper exception handling for zero division |

## Configuration Files

### pyproject.toml
- Defines package metadata and dependencies
- Configures optional test dependencies
- Includes Tox configuration for testing

### requirements.txt
- Simple dependency list for manual installation
- Contains only `nose2` for testing

## Development Workflow

1. **Make Changes**: Modify code in the `app/` directory
2. **Write Tests**: Add corresponding tests in `tests/`
3. **Run Tests**: Execute `nose2 -v` to verify functionality
4. **Check Coverage**: Use coverage tools to ensure complete testing

## Learning Objectives

This demonstration helps you understand:

1. **Project Structure**: How to organize a testable Python package
2. **Test Discovery**: How Nose2 finds and runs tests automatically
3. **Assertions**: Using unittest assertions for test validation
4. **Exception Testing**: Testing error conditions and exception handling
5. **Package Imports**: Managing imports and exports in Python packages

## Common Commands Reference

```bash
# Install package in development mode
pip install -e .[test]

# Run all tests with verbose output
nose2 -v

# Run tests with timing information
nose2 -v --verbose

# Check if package can be imported correctly
python -c "from app import add, subtract, multiply, divide; print('Import successful')"

# Test specific functionality interactively
python -c "from app.calculator import add; print(f'2 + 3 = {add(2, 3)}')"
```

## Extending the Example

Try these exercises to learn more:

1. **Add New Functions**: Implement power, square root, or modulo operations
2. **Add More Tests**: Create tests for edge cases like very large numbers
3. **Add Test Fixtures**: Use setUp/tearDown methods for test preparation
4. **Add Parameterized Tests**: Use Nose2's params decorator for multiple test cases
5. **Add Mocking**: Mock external dependencies if you add file I/O or network calls

## Troubleshooting

### Common Issues

**Import Errors**: 
```bash
# Make sure you're in the correct directory
cd math_utils
# Ensure package is properly installed
pip install -e .[test]
```

**Test Discovery Issues**:
```bash
# Run from the package root directory
nose2 -v tests
# Or specify the start directory
nose2 -s tests
```

**Module Not Found**:
```bash
# Check Python path or use relative imports
python -m nose2 tests.test_calculator
```

## Next Steps

After exploring this example:
1. Try modifying the calculator functions and updating tests
2. Add new mathematical operations and corresponding tests
3. Experiment with different test assertion methods
4. Practice test-driven development by writing tests before code
5. Explore Nose2's advanced features like plugins and configuration