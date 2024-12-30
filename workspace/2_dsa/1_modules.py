# Modules: a file containing code you want to include in your program
#   use 'import' to include a module (build-in or  your own)
#   useful to break up large program resuable separate files

# print(help("modules")) # available modules

import math as m
# from math import pi
import module_example as example


# print(pi)
print(m.pi) # 3.141592653589793
print(m.e) # 2.718281828459045

print

a,b,c,d,e = 1,2,3,4,5

print(m.e ** a) # 2.718281828459045
print(m.e ** b) # 7.3890560989306495
print(m.e ** c) # 20.085536923187664
print(m.e ** d) # 54.59815003314423
print(m.e ** e) # 148.41315910257657

# example module
print()
pi = example.pi
square = example.square(3)
cube = example.cube(3)
circumference = example.circumference(3)
area = example.area(3)

print(pi) # 3.14159
print(square) # 9
print(cube) # 27
print(circumference) # 18.849539999999998
print(area) # 28.27431
