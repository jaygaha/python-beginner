# @property
# @property is a built-in decorator in Python which is helpful in defining the properties effortlessly without calling the property() function explicitly.
# Decorator used to dfine a method as a property. (it can be accessed as an attribute instead of a method)
# Benefits:
# - Add additional logic when read, write or delete a property
# - gives you getter, setter, deleter methods

class Reactangle:
    def __init__(self, width, height):
        # _width and _height are private variables, they are not accessible from outside the class
        self._width = width
        self._height = height

    # Getter
    @property
    def width(self):
        return f"{self._width:.1f}cm"

    @property
    def height(self):
        return f"{self._height:.1f}cm"

    # Setter
    @width.setter
    def width(self, new_width):
        if new_width > 0:
            self._width = new_width
        else:
            print("Width must be greater than 0")

    @height.setter
    def height(self, new_height):
        if new_height > 0:
            self._height = new_height
        else:
            print("Height must be greater than 0")


    # Deleter
    @width.deleter
    def width(self):
        del self._width
        print("Width has been deleted")

    @height.deleter
    def height(self):
        del self._height
        print("Height has been deleted")

rectangle = Reactangle(10, 20)

rectangle.width = 40
rectangle.height = 70

del rectangle.width
del rectangle.height

# print(rectangle.width)
# print(rectangle.height)