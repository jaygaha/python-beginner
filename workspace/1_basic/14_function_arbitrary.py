# *args     = allows to pass multiple non-key arguments
# **kwargs = allows to pass multiple keyword argument
#             * unpacking operator
# 1. positional, 2. default, 3. keyword, 4. arbitrary

# arbitrary

#*args
def add(*nums):
    total = 0
    for num in nums:
        total += num
    return total

print(add(1, 2, 3)) # 6
print(add(1, 2, 3, 4)) # 10

def display_name(*args):
    for arg in args:
        print(arg, end=" ")


display_name("Dr.", "John", "Doe")

print()

# **kwargs

def print_address(**kwargs):
    # print(type(kwargs)) #  <class 'dict'>
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_address(street="3-19-2", city="Tokyo", zip="172-0002", apartment="Grand apartment")