# Recursion:  The act or process of returning or running back

def countdown(n):
    while n >= 0:
        print(n)
        n -= 1


print(countdown(5)) # 5 4 3 2 1 0

# Calculate Factorial

def factorial(n):
    print(f"factorial() called with n = {n}")
    return_value = 1 if n <= 1 else n * factorial(n -1)
    print(f"-> factorial({n}) returns {return_value}")

    return return_value

print(factorial(6))

'''
factorial() called with n = 6
factorial() called with n = 5
factorial() called with n = 4
factorial() called with n = 3
factorial() called with n = 2
factorial() called with n = 1
-> factorial(1) returns 1
-> factorial(2) returns 2
-> factorial(3) returns 6
-> factorial(4) returns 24
-> factorial(5) returns 120
-> factorial(6) returns 720
720
'''

# using a for loop
def factorial_loop(n):
    return_value = 1
    for i in range(2, n + 1):
        return_value *= i

    return return_value

# Output
print(factorial_loop(6)) # 720

# reduce()
from functools import reduce

def factorial_reduce(n):
    return reduce(lambda x,y: x * y, range(1, n+1) or [1])

print(factorial_reduce(4)) # 24

# math module
from math import factorial as factMath

print(factMath(6)) # 720

# Speed Comparison
# timeit(<command>, setup=<setup_string>, number=<iterations>)
from timeit import timeit

setup_string = """
print("Recursive:")
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)
"""

print(timeit("factorial(4)", setup=setup_string, number=10000000))

'''
Recursive:
10.3782601999701
'''