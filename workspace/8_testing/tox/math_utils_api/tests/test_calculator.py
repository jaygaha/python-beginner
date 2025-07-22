"""
Test calculator module for math_utils app.
"""

import pytest

from app.calculator import add, divide, multiply, subtract


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(3, 5) == -2


def test_multiply():
    assert multiply(2, 3) == 6
    assert multiply(-1, 1) == -1


def test_divide():
    assert divide(6, 3) == 2
    assert divide(3, 6) == 0.5
    assert divide(0, 1) == 0


def test_divide_by_zero():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(5, 0)
