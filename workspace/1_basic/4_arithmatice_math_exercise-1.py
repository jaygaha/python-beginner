# Exercise 1: Circumference and Area of a Circle

import math

radius = float(input("Enter the radius of the circle: "))

circumference = 2 * math.pi * radius
# area = math.pi * radius ** 2
area = math.pi * pow(radius, 2)

# print(f"Circumference of the circle is {circumference:.2f}")
# print(f"Area of the circle is {area:.2f}")
print(f"Circumference of the circle is {round(circumference,2)}cm")
print(f"Area of the circle is {round(area,2)}cm^2")
