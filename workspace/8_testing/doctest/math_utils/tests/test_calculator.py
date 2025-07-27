"""
Unit tests for calculator module using doctest.
"""

import doctest
import unittest
from app.calculator import add, subtract, multiply, divide


class TestCalculator(unittest.TestCase):
    """Test cases for calculator functions."""

    def test_add(self):
        """Test addition function."""
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)
        self.assertEqual(add(0, 0), 0)
        self.assertEqual(add(-5, -3), -8)

    def test_subtract(self):
        """Test subtraction function."""
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)
        self.assertEqual(subtract(0, 0), 0)
        self.assertEqual(subtract(-3, -5), 2)

    def test_multiply(self):
        """Test multiplication function."""
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-2, 3), -6)
        self.assertEqual(multiply(0, 5), 0)
        self.assertEqual(multiply(-2, -3), 6)

    def test_divide(self):
        """Test division function."""
        self.assertEqual(divide(6, 3), 2.0)
        self.assertEqual(divide(5, 2), 2.5)
        self.assertEqual(divide(-6, 3), -2.0)
        self.assertEqual(divide(0, 5), 0.0)

    def test_divide_by_zero(self):
        """Test division by zero raises ValueError."""
        with self.assertRaises(ValueError) as context:
            divide(10, 0)
        self.assertEqual(str(context.exception), "Cannot divide by zero")


def load_tests(loader, tests, ignore):
    """Load doctests from calculator module."""
    # Import the calculator module for doctest
    from app import calculator

    # Add doctests to the test suite
    tests.addTests(doctest.DocTestSuite(calculator))
    return tests


if __name__ == '__main__':
    # Run both unit tests and doctests
    unittest.main(verbosity=2)
