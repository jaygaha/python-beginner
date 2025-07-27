"""
Simple calculator module for math_utils app.
"""

def add(a, b):
    """
    Add two numbers.

    >>> add(2, 3)
    5
    >>> add(-1, 1)
    0
    """
    return a + b

def subtract(a, b):
    """
    Subtract b from a.

    >>> subtract(5, 3)
    2
    >>> subtract(3, 5)
    -2
    """
    return a - b

def multiply(a, b):
    """
    Multiply two numbers.

    >>> multiply(2, 3)
    6
    >>> multiply(-2, 3)
    -6
    """
    return a * b

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
