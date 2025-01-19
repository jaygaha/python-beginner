# Generator Expressions

# A generator expression is a compact way to create a generator
# A generator expression is written like a list comprehension, but with parentheses instead of square brackets
# The result is a generator object that can be used to iterate over the values

sq_list = [x**2 for x in range(10)] # this produces a list of the squares of the numbers from 0 to 9

print(sq_list) # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

sq_iterator = (x**2 for x in range(10)) # this produces a generator object that can be used to iterate over the squares of the numbers from 0 to 9

print(sq_iterator) # <generator object <genexpr> at 0x7f8b0e3b0b50>

print(sq_iterator.__next__()) # 0
print(sq_iterator.__next__()) # 1