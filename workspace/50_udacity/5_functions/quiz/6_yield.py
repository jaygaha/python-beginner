# Yield
#
# yield: a function that returns a generator
# next: a function that returns the next value in a generator
# range: a function that returns a series of numbers
# This statement is what makes a function a generator
#
# generator: a function that returns a series of values

def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fib = fibonacci()

for i in range(10):
    print(next(fib))
