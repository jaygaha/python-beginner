# Python Iterators: __iter__() and __next()__ methods
# an iterator is an object that contains a countable number of values

# Tuple is an iterable object
my_tuple = ("Red", "Green", "Blue")
my_iter = iter(my_tuple)

print(next(my_iter)) # Red
print(next(my_iter)) # Green
print(next(my_iter)) # Blue

# String is an iterable object
my_string = "Python"
my_iter = iter(my_string)

print(next(my_iter)) # P
print(next(my_iter)) # y
print(next(my_iter)) # t
print(next(my_iter)) # h
print(next(my_iter)) # o
print(next(my_iter)) # n

# Looping through an iterator
# The for loop actually creates an iterator object and executes the next() method for each loop.
for x in my_tuple:
    print(x)

# iterate the characters of a string
for x in my_string:
    print(x)
