# Static Typing: The type of a variable is known at compile time

# Typing: Typing is a module in Python that provides support for type hints and type checking.
# It provides a way to specify the type of a variable or function parameter.

# Type hints: A type hint is a comment that specifies the type of a variable or function parameter.
# Example
def headline(text: str, align: bool = True) -> str:
    if align:
        return f"{text.title()}\n{'-' * len(text)}"
    else:
        return f" {text.title()} ".center(50, "x")

print(headline("hello world",)) # Hello World
print(headline("hello world", align=False)) # xxxxxxxxxxxxxxxxxx Hello World xxxxxxxxxxxxxxxxxxx

'''
# _mypy_: A static type checker for Python
# pip install mypy
# usage: mypy <filename>
'''

print(headline("use mypy", align="center")) # Error : Argument 2 to "headline" has incompatible type "str"; expected "bool"
print(headline("use mypy", align=False))
print()

# cosine
import numpy as np

def print_cosine(angle: np.ndarray) -> None:
    with np.printoptions(precision=3, suppress=True):
        print(np.cos(angle))

x = np.linspace(0, 2 * np.pi, 9)
print_cosine(x) # [ 1.     0.707  0.    -0.707 -1.    -0.707 -0.     0.707  1.   ]


#
def sum_numbsers(a: int, b: int) -> int:
    return a + b

print(sum_numbsers(10, 2))
print(sum_numbsers(10.5, 2))
print(sum_numbsers("John", "Laure"))

# Variable annotation:
# A variable annotation is a type hint that specifies the type of a variable.
name: str = "John"
age: int = 20
grade: float = 3.5
is_adult: bool = True

print(name, age, grade, is_adult) # John 20 3.5 True

# Advanced typing:
# A variable annotation can also be used to specify the type of a function parameter.
from typing import List, Dict, Tuple

names: List[str] = ["John", "Jane", "Bob"]
ages: Dict[str, int] = {"John": 20, "Jane": 21, "Bob": 22}
coordinates: Tuple[float, float] = (1.0, 2.0)

print(names, ages, coordinates) # ['John', 'Jane', 'Bob'] {'John': 20, 'Jane': 21, 'Bob': 22} (1.0, 2.0)

# function annotation:
# A function annotation is a type hint that specifies the type of a function.
def list_sum(numbers: List[int]) -> int:
    return sum(numbers)

print(list_sum([1, 2, 3, 4, 5])) # 15
