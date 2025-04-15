# Build a Polygon Area Calculator Project
# Ref: https://www.freecodecamp.org/learn/scientific-computing-with-python/build-a-polygon-area-calculator-project/build-a-polygon-area-calculator-project

class Rectangle:
    def __init__(self, width, height):
        # initialize the width and height of the rectangle
        self.width = width
        self.height = height

    def set_width(self, width):
        self.width = width

    def set_height(self, height):
        self.height = height

    # area: width * height
    def get_area(self):
        return self.width * self.height

    # perimeter: (2 * width) + (2 * height)
    def get_perimeter(self):
        return (2 * self.width) + (2 * self.height)

    # diagonal: ((width ** 2 + height ** 2) ** .5)
    def get_diagonal(self):
        return (self.width ** 2 + self.height ** 2) ** .5

    # Returns a string that represents the shape using lines of '*'.
    def get_picture(self):
        # genereate a string of '*' with the length of the width and height
        # limit for picture is 50 characters from the left and right
        if self.width > 50 or self.height > 50:
            return "Too big for picture."

        return ('*' * self.width + '\n') * self.height  # Create the picture

    # Takes another shape (sq or react) as argument and returns the number of times the passed in shape
    # could fit inside the shape(with no rotations)
    def get_amount_inside(self, sq):
        return (self.width // sq.width) * (self.height // sq.height)

    def __str__(self):
        # string representation of the rectangle
        return f"Rectangle(width={self.width}, height={self.height})"

# Subclass of Rectangle
class Square(Rectangle):
    def __init__(self, side):
        # init the sq with single side length
        super().__init__(side, side) # calling the react constructor with equal width and height

    def set_side(self, side):
        # set both width and height to the same value
        self.set_width(side)
        self.set_height(side)

    def set_width(self, width):
        # Override to ensure width and height remain equal
        super().set_width(width)
        super().set_height(width)

    def set_height(self, height):
        # Override to ensure width and height remain equal
        super().set_width(height)
        super().set_height(height)

    def __str__(self):
        # string representation of the square
        return f"Square(side={self.width})"

if __name__ == "__main__":
    rect = Rectangle(10, 5)
    print(rect.get_area()) # 50
    rect.set_height(3)
    print(rect.get_perimeter()) # 26
    print(rect) # Rectangle(width=10, height=3)
    print(rect.get_picture())
    # **********
    # **********
    # **********

    sq = Square(9)
    print(sq.get_area()) # 81
    sq.set_side(4)
    print(sq.get_diagonal()) # 5.656854249492381
    print(sq) # Square(side=4)
    print(sq.get_picture())
    # ****
    # ****
    # ****
    # ****

    rect.set_height(8)
    rect.set_width(16)
    print(rect.get_amount_inside(sq)) # 8
