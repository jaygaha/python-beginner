# Generators
#
# A generator is a function that returns an iterator
#
# iterator: an object that can be used to iterate over a sequence

def generate_numbers():
    for i in range(10):
        yield i

numbers = generate_numbers()
print(next(numbers))
print(next(numbers))
