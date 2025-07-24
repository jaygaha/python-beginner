import unittest
from app.calculator import add, subtract, multiply, divide

"""
Test cases for the Calculator class.

Nose2 uses unittest-style tests. Files must start with test_ for discovery.
Tests are written as unittest.TestCase subclasses, using methods like assertEqual.
"""

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(-1, 1), -1)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(3, 6), 0.5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(5, 0)
