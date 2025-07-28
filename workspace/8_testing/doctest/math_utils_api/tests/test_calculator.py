"""
Unit tests for calculator module using pytest.

Note: doctests from app.calculator are automatically discovered and run by pytest.
"""

import pytest
from app.calculator import add, subtract, multiply, divide


def test_add():
    """Test addition function."""
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(-5, -3) == -8


def test_subtract():
    """Test subtraction function."""
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2
    assert subtract(0, 0) == 0
    assert subtract(-3, -5) == 2


def test_multiply():
    """Test multiplication function."""
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(0, 5) == 0
    assert multiply(-2, -3) == 6


def test_divide():
    """Test division function."""
    assert divide(6, 3) == 2.0
    assert divide(5, 2) == 2.5
    assert divide(-6, 3) == -2.0
    assert divide(0, 5) == 0.0


def test_divide_by_zero():
    """Test division by zero raises ValueError."""
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
