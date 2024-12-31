# super(): function used in a child class to call methods from a parent class (superclass)
# allows to extend the functionality of the inherited methods

class Shape:
    def __init__(self, color, is_filled):
        self.color = color
        self.is_filled = is_filled

    def describe(self):
        print(f"It is {self.color} and {'filled' if self.is_filled else 'not filled'}")

class Circle(Shape):
    def __init__(self, color, is_filled, radius):
        super().__init__(color, is_filled)
        self.radius = radius

    # Method overriding
    def describe(self):
        print(f"It is a circle with an area of {3.14159 * self.radius * self.radius:.02f}cm^2")
        super().describe()


class Square(Shape):
    def __init__(self, color, is_filled, width):
        super().__init__(color, is_filled)
        self.width = width

    # Method overriding
    def describe(self):
        print(f"It is a square with an area of {self.width * self.width:.02f}cm^2")
        super().describe()

class Triangle(Shape):
    def __init__(self, color, is_filled, width, height):
        super().__init__(color, is_filled)
        self.width = width
        self.height = height

    # Method overriding
    def describe(self):
        print(f"It is a triangle with an area of {(self.width * self.height)/2:.02f}cm^2")
        super().describe()

circe = Circle(color="red", is_filled=True, radius=5)
square = Square("green", False, 8)
triangle = Triangle("blue", True, 4, 8)

print(circe.color)

print()
print(square.color)
print(square.is_filled)
print(f"{square.width}cm")

print()
print(triangle.color)
print(triangle.is_filled)
print(f"{triangle.width}cm")
print(f"{triangle.height}cm")

print()
circe.describe()

print()
square.describe()
print()
triangle.describe()