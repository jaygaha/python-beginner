# Math Utils Library

A simple Python library for basic mathematical operations with comprehensive test coverage.

## Overview

Math Utils is a beginner-friendly Python package that demonstrates fundamental programming concepts including:
- Function implementation
- Error handling
- Unit testing with Python's `unittest` framework
- Package structure and organization

## Features

- **Basic Calculator Operations**: Addition, subtraction, multiplication, and division
- **Error Handling**: Proper exception handling for edge cases like division by zero
- **Comprehensive Testing**: Full test coverage with multiple test cases
- **Clean Code Structure**: Well-organized package with proper imports and documentation

## Installation

Clone the repository and navigate to the math_utils directory:

```bash
cd python-beginner/workspace/8_testing/pytest/math_utils
```

No additional dependencies are required as this project uses Python's built-in modules.

## Usage

### Basic Usage

```python
from app.calculator import add, subtract, multiply, divide

# Addition
result = add(5, 3)        # Returns: 8
result = add(-2, 7)       # Returns: 5
result = add(0, 0)        # Returns: 0

# Subtraction
result = subtract(10, 4)  # Returns: 6
result = subtract(3, 8)   # Returns: -5
result = subtract(0, 0)   # Returns: 0

# Multiplication
result = multiply(4, 6)   # Returns: 24
result = multiply(-3, 4)  # Returns: -12
result = multiply(0, 100) # Returns: 0

# Division
result = divide(15, 3)    # Returns: 5.0
result = divide(10, 4)    # Returns: 2.5
result = divide(-8, 2)    # Returns: -4.0
```

### Using the Package Import

```python
from app import add, subtract, multiply, divide

# All functions are available directly
sum_result = add(10, 20)
diff_result = subtract(50, 30)
product_result = multiply(7, 8)
quotient_result = divide(100, 25)
```

### Error Handling

The library includes proper error handling for invalid operations:

```python
from app.calculator import divide

try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Error: {e}")  # Output: Error: Cannot divide by zero
```

## Function Reference

### `add(a, b)`
Adds two numbers together.

**Parameters:**
- `a` (int/float): First number
- `b` (int/float): Second number

**Returns:**
- `int/float`: Sum of a and b

**Example:**
```python
add(5, 3)    # Returns: 8
add(2.5, 1.5)  # Returns: 4.0
```

### `subtract(a, b)`
Subtracts the second number from the first.

**Parameters:**
- `a` (int/float): Number to subtract from
- `b` (int/float): Number to subtract

**Returns:**
- `int/float`: Difference of a and b

**Example:**
```python
subtract(10, 3)  # Returns: 7
subtract(5, 8)   # Returns: -3
```

### `multiply(a, b)`
Multiplies two numbers together.

**Parameters:**
- `a` (int/float): First number
- `b` (int/float): Second number

**Returns:**
- `int/float`: Product of a and b

**Example:**
```python
multiply(4, 5)   # Returns: 20
multiply(-3, 2)  # Returns: -6
```

### `divide(a, b)`
Divides the first number by the second.

**Parameters:**
- `a` (int/float): Dividend (number to be divided)
- `b` (int/float): Divisor (number to divide by)

**Returns:**
- `float`: Quotient of a divided by b

**Raises:**
- `ValueError`: If b is 0 (division by zero)

**Example:**
```python
divide(10, 2)   # Returns: 5.0
divide(7, 3)    # Returns: 2.333...
divide(10, 0)   # Raises: ValueError: Cannot divide by zero
```

## Project Structure

```
math_utils/
├── README.md              # This documentation file
├── pyproject.toml        # Project configuration
├── requirements.txt      # Dependencies (empty - no external deps)
├── app/                  # Main application package
│   ├── __init__.py      # Package initialization with exports
│   └── calculator.py    # Core calculator functions
└── tests/               # Test suite
    ├── __init__.py     # Test package initialization
    └── test_calculator.py  # Unit tests for calculator functions
```

## Testing

This project includes comprehensive unit tests using Python's `unittest` framework.

### Running Tests

```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_calculator

# Run with verbose output
python -m unittest tests.test_calculator -v

# Run a specific test method
python -m unittest tests.test_calculator.TestCalculator.test_add
```

### Test Coverage

The test suite covers:

- **Addition Tests**: Positive numbers, negative numbers, zero values
- **Subtraction Tests**: Various combinations including negative results
- **Multiplication Tests**: Positive, negative, and zero multiplication
- **Division Tests**: Normal division, negative numbers, edge cases
- **Error Handling Tests**: Division by zero exception testing

### Test Examples

```python
class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(9, 9), 18)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(6, 0)
```

## Development

### Code Style
- Functions use clear, descriptive names
- Proper docstrings for documentation
- Consistent parameter naming
- Comprehensive error handling

### Best Practices Demonstrated
- **Separation of Concerns**: Logic separated from tests
- **Error Handling**: Proper exception handling with meaningful messages
- **Testing**: Comprehensive test coverage with edge cases
- **Documentation**: Clear documentation and examples
- **Package Structure**: Proper Python package organization

## Educational Value

This project is designed for beginners to learn:

1. **Function Definition**: How to create reusable functions
2. **Parameter Handling**: Working with function parameters
3. **Return Values**: Returning computed results
4. **Exception Handling**: Using try/except and raising exceptions
5. **Testing**: Writing and running unit tests
6. **Package Organization**: Structuring Python projects
7. **Documentation**: Writing clear README files and docstrings

## Common Use Cases

- Learning basic Python programming
- Understanding function implementation
- Practicing unit testing
- Exploring package structure
- Teaching programming fundamentals

## Extending the Library

You can extend this library by adding more mathematical operations:

```python
def power(base, exponent):
    """Calculate base raised to the power of exponent."""
    return base ** exponent

def square_root(number):
    """Calculate the square root of a number."""
    if number < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return number ** 0.5
```

Remember to add corresponding tests for any new functions!

## Contributing

When adding new features:
1. Implement the function in `app/calculator.py`
2. Add the function to `app/__init__.py` exports
3. Write comprehensive tests in `tests/test_calculator.py`
4. Update this README with documentation
5. Run all tests to ensure nothing breaks

## License

This project is for educational purposes and is part of the Python beginner learning materials.

---

**Happy coding!** 🐍