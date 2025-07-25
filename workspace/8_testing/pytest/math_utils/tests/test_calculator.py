import unittest
from app.calculator import add, subtract, multiply, divide

class TestCalculator(unittest.TestCase):
    def test_add(self):
        self.assertEqual(add(2, 3), 5)
        self.assertEqual(add(9, 9), 18)
        self.assertEqual(add(-1, 1), 0)


    def test_subtract(self):
        self.assertEqual(subtract(5, 3), 2)
        self.assertEqual(subtract(3, 5), -2)
        self.assertEqual(subtract(0, 0), 0)
        self.assertEqual(subtract(10, 5), 5)

    def test_multiply(self):
        self.assertEqual(multiply(2, 3), 6)
        self.assertEqual(multiply(0, 0), 0)
        self.assertEqual(multiply(-1, 1), -1)
        self.assertEqual(multiply(10, 5), 50)

    def test_divide(self):
        self.assertEqual(divide(6, 3), 2)
        self.assertEqual(divide(0, 1), 0)
        self.assertEqual(divide(-10, 2), -5)
        self.assertEqual(divide(10, -2), -5)
        self.assertEqual(divide(10, 5), 2)
        self.assertEqual(divide(10, 1), 10)
        self.assertEqual(divide(10, 10), 1)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            divide(6, 0)
