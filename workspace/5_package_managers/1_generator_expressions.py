# Generator Expressions
# Generator expressions are a high-performance, memory-efficient generalization of list comprehensions and generators.
# They are useful for creating sequences that are used only once and do not need to be stored in memory.
# Generator expressions are surrounded by parentheses and use the same syntax as list comprehensions,
# but with parentheses instead of square brackets.

# Generator: (expression for item in iterable)

def top_ten():

    yield 2
    yield 4
    yield 5

values = top_ten()
print(values)  # <generator object top_ten at 0x0000020C5D0A5F90>

print(values.__next__())  # 2
print(values.__next__())  # 4
print(values.__next__())  # 5

# Iterating over a generator
values = top_ten()

for i in values:
    print(i)

print()
def top_ten_sq():

    n = 1
    while n <= 10:
        sq = n*n
        yield sq
        n += 1

values = top_ten_sq()

for i in values:
    print(i)

