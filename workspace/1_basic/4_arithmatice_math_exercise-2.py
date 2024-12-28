# Exercise 2: Hypotenuse of a Right Triangle

import math

side1 = float(input("Enter the length of side 1: "))
side2 = float(input("Enter the length of side 2: "))

# hypotenuse = math.sqrt(side1 ** 2 + side2 ** 2)
hypotenuse = math.sqrt(pow(side1, 2) + pow(side2, 2))

print(f"The length of the hypotenuse is {round(hypotenuse,2)}cm")