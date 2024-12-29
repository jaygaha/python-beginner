# Iterables: An object/collection that can return its element one at a time, allowing it to be iterated over in a loop

# List
numbers = [1, 2, 3, 4, 5]

for number in reversed(numbers):
    print(number) # 5, 4, 3, 2, 1

print()

# Tuple
numbers = (1, 2, 3, 4, 5)

for number in numbers:
    print(number) # 1, 2, 3, 4, 5

# Set
fruits = {"apple", "banana", "orange", "coconut"}

for fruit in fruits:
    print(fruit)

print()

# String
name = "John Doe"

for character in name:
    print(character, end="-") # J-o-h-n- -D-o-e-

print()

# dictionery
my_dictionery = {"A": 1, "B": 2, "C": 3}

for key in my_dictionery:
    print(key) # A, B, C

print()

for value in my_dictionery.values():
    print(value, end=" ") # 1, 2, 3

print()

for key, value in my_dictionery.items():
    print(f"{key}: {value}")