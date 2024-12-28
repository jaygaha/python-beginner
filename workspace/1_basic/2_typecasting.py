# Typecasting
# Typecasting is the process of converting one data type to another.
# In Python, we can convert one data type to another using the following functions:
# int()
# float()
# str()
# bool()

name = "John Doe"
age = 22
height = 5.8
is_adult = True

# type: to get the data type of a variable
print(type(name)) # <class 'str'>
print(type(age)) # <class 'int'>
print(type(height)) # <class 'float'>
print(type(is_adult)) # <class 'bool'>

# Examples
height = int(height)

print(height) # 5

age = float(age)

print(age) # 22.0

age = str(age)

print(age) # 22.0
print(type(age)) # <class 'str'>

name = bool(name)

print(name) # True
print(type(name)) # <class 'bool'>