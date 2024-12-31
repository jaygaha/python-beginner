# Python Object Oriented Programming
# Object = A "bundle" of related attributes (variables) and methods (functions)
# Ex.: phone, cup, book
# You need a "class" to create many objects

# class = (blueprint) used to design the structure and layout of an object

from car import Car


car1 = Car('Mustang', 2004, 'red', False)
car2 = Car('Corvette', 2024, 'blue', True)

# print(car1.model)
# print(car2.model)

print(car1.drive())
# print(car2.stop())
print(car2.describe())