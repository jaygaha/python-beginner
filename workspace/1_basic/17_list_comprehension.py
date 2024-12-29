# List comprehension: A concise way to create lists in Python
# Compact and easier to read than tranditional loops
# [expression for value in iterable if condition]


# traditional loop
# doubles = []

# for x in range(1, 11):
#     doubles.append(x * 2)

# print(doubles) # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]

doubles = [x * 2 for x in range(1, 11)]
triples = [x * 3 for x in range(1, 11)]
squares = [z * z for z in range(1, 11)]

print(doubles) # [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
print(triples) # [3, 6, 9, 12, 15, 18, 21, 24, 27, 30]
print(squares) # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# Strings
fruits = ["apple", "banana", "orange", "coconut"]
fruits = [fruit.upper() for fruit in fruits]
fruit_chars = [fruit[0] for fruit in fruits]

print(fruits) # ['APPLE', 'BANANA', 'ORANGE', 'COCONUT']
print(fruit_chars) # ['A', 'B', 'O', 'C']

print()

numbers = [1,-2,4,-8,9]

positive_nums = [num for num in numbers if num >= 0]
negative_nums = [num for num in numbers if num < 0]
even_nums = [num for num in numbers if num % 2 == 0]
odd_nums = [num for num in numbers if num % 2 == 1]

print(positive_nums) # [1, 4, 9]
print(negative_nums) # [-2, -8]
print(even_nums) # [-2, 4,-8]
print(odd_nums) # [1, 9]

print()

grades = [43, 78, 98,30, 62, 53]
passing_grades = [grade for grade in grades if grade >= 60]

print(grades)

