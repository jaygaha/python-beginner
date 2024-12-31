# Polymorphism: Greek word that means to 'have many forms or faces'
#       Poly -> Many
#       Morphe -> Form
#
#       Two ways to achieve it
#       1. Inheritance: an object could be treated of the same types as a parent class
#       2. "Duck typing": Object must have necessary attributes/methods

# 1. Inheritance

from abc import ABC, abstractmethod

class Shape:

    @abstractmethod
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

class Trianle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return self.base * self.height * 0.5

class Pizza(Circle):
    def __init__(self, topping, radius):
        self.topping = topping
        super().__init__(radius)

shapes = [Circle(4), Square(5), Trianle(4, 5), Pizza("pepperoni", 14)]

for shape in shapes:
    print(f"{shape.area():.02f}cm^2")