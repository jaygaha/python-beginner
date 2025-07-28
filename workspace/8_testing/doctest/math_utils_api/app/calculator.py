"""
Simple calculator module for math_utils app.
"""


def add(a, b):
    """
    Adds two numbers together.

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b


def subtract(a, b):
    """
    Subtracts one number from another.

    >>> subtract(5, 3)
    2
    >>> subtract(3, 5)
    -2
    """
    return a - b


def multiply(a, b):
    """
    Multiplies two numbers.

    >>> multiply(2, 3)
    6
    >>> multiply(-2, 3)
    -6
    """
    return a * b


def divide(a, b):
    """
    Divides one number by another.

    >>> divide(6, 3)
    2.0
    >>> divide(10, 0)
    Traceback (most recent call last):
        ...
    ValueError: Cannot divide by zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
