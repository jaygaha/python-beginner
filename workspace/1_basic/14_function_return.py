# return = statement used to end a function and sent a result back to the caller

# positional
def add(x, y):
    z = x + y
    return z

def substract(x, y):
    z = x - y
    return z

def multiply(x, y):
    z = x * y
    return z

def divide(x, y):
    z = x / y
    return z

print(add(1, 2)) # 3
print(substract(1, 2)) # -1
print(multiply(1, 2)) # 2
print(divide(1, 2)) # 0.5

def create_name(first, last):
    first = first.capitalize()
    last = last.capitalize()

    return first + " " + last

full_name = create_name("john", "doe")

print(full_name)