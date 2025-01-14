# List Comprehensions
#
# List comprehensions are a concise way to create lists in Python. They are
# syntactically similar to list literals, but they are enclosed in square
# brackets and can contain an arbitrary number of expressions. The expressions
# are separated by commas and the result is a list of the expressions evaluated
# from left to right.
#
# For example, the following list comprehension creates a list of the squares
# of the numbers from 1 to 10:
#
# [x**2 for x in range(1, 11)]
#
# The result is [1, 4, 9, 16, 25, 36, 49, 64, 81, 100].

# WITH IF
squares = [x**2 for x in range(9) if x % 2 == 0]
print(squares) # [0, 4, 16, 36, 64]

# with else
squares = [x**2 if x % 2 == 0 else x + 3 for x in range(9)]
print(squares) # [0, 4, 4, 6, 16, 8, 36, 10, 64]


# Quiz: Extract First Names
names = ["Rick Sanchez", "Morty Smith", "Summer Smith", "Jerry Smith", "Beth Smith"]

# first_names = [name.lower().split()[0] for name in names]
first_names = [name.split()[0].lower() for name in names]
print(first_names) # ['Rick', 'Morty', 'Summer', 'Jerry', 'Beth']

# Quiz: Multiples of Three
# multiples_of_three = [x for x in range(10) if x % 3 == 0]
# print(multiples_of_three) # [0, 3, 6, 9]

multiples_3 = [3 * i for i in range(1, 21)]
print(multiples_3) # [0, 3, 6, 9, 12, 15, 18]

# Quiz: Filter Names by Scores
scores = {
             "Rick Sanchez": 70,
             "Morty Smith": 35,
             "Summer Smith": 82,
             "Jerry Smith": 23,
             "Beth Smith": 98
          }

passed = [name for name, score in scores.items() if score >= 65] #
print(passed) # ['Rick Sanchez', 'Summer Smith', 'Beth Smith']
