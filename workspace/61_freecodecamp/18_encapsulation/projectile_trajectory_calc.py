# Learn Encapsulation by Building a Projectile Trajectory Calculator
# Encapsulation is a code OOP principle based on writing code that limits direct access to data and methods.
# Ref: https://www.freecodecamp.org/learn/scientific-computing-with-python/learn-encapsulation-by-building-a-projectile-trajectory-calculator/step-1

# Build a program that calculates and display the trajectory of a projectile
# given the angle, speed and height of the throw.

import math

GRAVITATIONAL_ACCELERATION = 9.81
PROJECTILE = "∙"
x_axis_tick = "T"
y_axis_tick = "⊣"

class Projectile:
    # __slots__: assin it a squuence of strings restricts the creation of attributes to thoese included in that sequence
    # assign as tupple
    __slots__ = ('__speed', '__height', '__angle')

    def __init__(self, speed, height, angle):
        self.__speed = speed # __ denotes private
        self.__height = height
        self.__angle = math.radians(angle) # convert to radians from degrees

    # calculates the displacement of the projectile;
    # which is the horizontal space travleled from the throw to when the projectile tpuches the ground
    def __calculate_displacement(self):
        horizontal_component = self.__speed * math.cos(self.__angle)
        vertical_component = self.__speed * math.sin(self.__angle)
        squared_displacement = vertical_component ** 2
        gh_comp = 2 * GRAVITATIONAL_ACCELERATION * self.__height
        sqrt_component = math.sqrt(squared_displacement + gh_comp)

        return horizontal_component * (vertical_component / sqrt_component) / GRAVITATIONAL_ACCELERATION

    # def __str__(self):
    #         return f'''
    # Projectile details:
    # speed: {self.__speed} m/s
    # height: {self.__height} m
    # angle: {round(math.degrees(self.__angle))}°
    # displacement: {round(self.__calculate_displacement(), 1)} m
    # '''

    # __str__ method refers to the attributes of the class direclty, use getters instead of direct attributes
    def __str__(self):
        return f'''
    Projectile details:
    speed: {self.speed} m/s
    height: {self.height} m
    angle: {self.angle}°
    displacement: {round(self.__calculate_displacement(), 1)} m
    '''

    # the formula to calculate the vertical position y for any given horizontal position x, having the starting angle θ, speed v0 and height y0
    # You will need to use math.tan() and math.cos() and remember that x ** y is the way to write xy
    # , and that the value of g is in the variable GRAVITATIONAL_ACCELERATION.
    def __calculate_y_coordinate(self, x):
        height_component = self.__height
        angle_component = math.tan(self.__angle) * x
        acceleration_component = GRAVITATIONAL_ACCELERATION * x ** 2 / (2 * self.__speed ** 2 * math.cos(self.__angle) ** 2)
        y_coordinate = height_component + angle_component - acceleration_component

        return y_coordinate

    # calculates the coordinates for all x values from 0 up to the displacement rounded up (not inclusive),
    #  and then returns them as a list of tuples (x, y).
    def calculate_all_coordinates(self):
        return [
            (x, self.__calculate_y_coordinate(x))
            for x in range(math.ceil(self.__calculate_displacement()))
        ]

    def __calculate_horizontal_position(self, y):
        return y / math.tan(self.__angle) - GRAVITATIONAL_ACCELERATION * self.__height / 2

    def __calculate_trajectory(self):
        # create a list of tuples
        trajectory = []
        x = 0
        y = self.__calculate_y_coordinate(x)
        trajectory.append((x, y))
        while y > 0:
            x = self.__calculate_horizontal_position(y)
            y = self.__calculate_y_coordinate(x)
            trajectory.append((x, y))
        return trajectory

    def __draw_trajectory(self):
        trajectory = self.__calculate_trajectory()
        print(f"{x_axis_tick}{y_axis_tick}")
        for x, y in trajectory:
            print(f"{x}{y}")

    # Getters are what can be used to get the value of a private attribute from outside the class
    # To define a getter, need to define method with @property decorator
    @property
    def speed(self):
        return self.__speed

    @property
    def height(self):
        return self.__height

    @property
    def angle(self):
        return round(math.degrees(self.__angle)) # convert to degrees from radians


    # Setters allows to set the value of a private attribute from outside the class in indirect way
    # To define a setter, need to define method with @propertyName.setter decorator
    @speed.setter
    def speed(self, new_speed):
        self.__speed = new_speed

    @height.setter
    def height(self, new_height):
        self.__height = new_height

    @angle.setter
    def angle(self, new_angle):
        self.__angle = math.radians(new_angle) # convert to radians from degrees

    # good practice to define a __repr__ method to return a string representation of the object
    # __str__ intended to be user friendly, while __repr__ is intended to be used for programmers
    def __repr__(self):
        return f"Projectile({self.speed}, {self.height}, {self.angle})"


class Graph:
    __slots__ = ('__coordinates')

    def __init__(self, coordinates):
        self.__coordinates = coordinates

    def __repr__(self):
        return f"Graph({self.__coordinates})"

    def create_coordinates_table(self):
        table = '\n  x      y\n'
        for x, y in self.__coordinates:
            table += f'{x:>3}{y:>7.2f}\n'

        return table

        # return a list of tuples
        # table = []
        # for x, y in self.__coordinates:
        #     table.append((x, y))
        # return table

    def create_trajectory(self):
        # local copy of the coordinates by converting rounded to int
        rounded_coords = [
            (round(x), round(y))
            for x, y in self.__coordinates
        ]

        # find max x and y
        x_max = max(rounded_coords, key=lambda x: x[0])[0]
        y_max = max(rounded_coords, key=lambda x: x[1])[1]

        # create a list of lists where the external list contains y_max + 1 lists each with inside x_max + 1 elements which is single space
        # matrix_list = [[' ' for _ in range(x_max + 1)] for _ in range(y_max + 1)]

        # for x, y in rounded_coords:
        #     matrix_list[y][x] = ' '

        matrix_list = [[' ' for _ in range(x_max + 1)] for _ in range(y_max + 1)]

        # use the list of coordinates in rounded_coords to change the elements in matrix_list at the coordinates in the list to the symbol in the PROJECTILE variable
        for x, y in rounded_coords:
            matrix_list[-y-1][x] = PROJECTILE

        # Join the inner lists to have a list of strings.
        matrix = [
            ''.join(row)
            for row in matrix_list
        ]

        # add thex and y axis to the graph using x_axis_tick and y_axis_tick
        matrix_axes = [y_axis_tick + row for row in matrix]
        matrix_axes.append(" " + x_axis_tick * (len(matrix[0])))

        graph = "\n" + "\n".join(matrix_axes) + "\n"

        return graph

# global helper function for projectile trajectory
# that takes in the desired values for speed, height and angle and prints to the terminal in sequence,
# the details of the projectile, the table of coordinates and the graph of the trajectory.
def projectile_helper(speed, height, angle):
    projectile = Projectile(speed, height, angle)
    coordinates = projectile.calculate_all_coordinates()

    graph = Graph(coordinates)
    print(projectile)
    print(graph.create_coordinates_table())
    print(graph.create_trajectory())

    return(projectile_helper)

if __name__ == "__main__":
    # ball = Projectile(10, 3, 45)
    # print(ball)
    # coordinates = ball.calculate_all_coordinates()

    # graph = Graph(coordinates)
    # # print(graph.create_coordinates_table())
    # # print(graph.create_trajectory())
    # # print with loop
    # # for x in graph.create_trajectory():
    # #     print(x)

    # print(graph.create_trajectory())

    # call the global helper function
    projectile_helper(10, 3, 45)
