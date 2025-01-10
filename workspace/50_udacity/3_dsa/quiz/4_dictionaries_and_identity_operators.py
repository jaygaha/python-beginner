# Dictionaries and Identity operators
# A dictionary is a mutable data type that stores mappings of unique keys to values. Here's a dictionary that stores elements and their atomic numbers.
# elements = {"hydrogen": 1, "helium": 2, "carbon": 6}

# Identity operators are operators that return the same value they are given. Here's an example of the identity operator.
# x = {"one": 1, "two": 2, "three": 3}
# s = x.get("one")
# print("four" in x) # evaluates to False
# print(s is None) # evaluates if both sides have the same identity
# print(s is not None) # evaluates if both sides have different identities

# Example:
population = {"Shanghai": 17.8, "Istanbul": 13.3, "Kathmandu": 13.0, "Mumbai": 12.5}

print(population)

print("Kathmandu" in population) # evaluates to True

# What happens if we look up a value that isn't in the dictionary? Create a test dictionary and use the square brackets to look up a value that you haven't defined. What happens?
# population = {"Shanghai": 17.8, "Istanbul": 13.3, "Kathmandu": 13.0, "Mumbai": 12.5}
# print(population["New York"]) # KeyError


a = [1, 2, 3]
b = a
c = [1, 2, 3]

print(a == b)
print(a is b)
print(a == c)
print(a is c) # evaluates to False, because a and c are different lists. They have different identities.

animals = {'dogs': [20, 10, 15, 8, 32, 15], 'cats': [3,4,2,8,2,4], 'rabbits': [2, 3, 3], 'fish': [0.3, 0.5, 0.8, 0.3, 1]}

print(type(animals))
print(type(animals['dogs']))
print(type(animals['dogs'][0]))

print(animals['dogs'])
print(animals['dogs'][3])

# print(animals[3]) # KeyError

# When to use dictionaries and when to use lists?
# Lists are great for storing ordered data. Dictionaries are great for storing unordered data.
#

# invalid dictionary - this should break
# room_numbers = {
#     ['Freddie', 'Jen']: 403,
#     ['Ned', 'Keith']: 391,
#     ['Kristin', 'Jazzmyne']: 411,
#     ['Eugene', 'Zach']: 395
# }
room_numbers = {
    'Freddie': 403,
    'Jen': 403,
    'Ned': 391,
    'Keith': 391,
    'Kristin': 411,
    'Jazzmyne': 411,
    'Eugene': 395,
    'Zach': 395
}

print(room_numbers)

# The dictionary above is invalid because it is using a mutable datatype (list) as a key.
# Correct! The error you saw was TypeError: unhashable type: 'list'. In Python, any immutable object (such as an integer, boolean, string, tuple) is hashable,
# meaning its value does not change during its lifetime. This allows Python to create a unique hash value to identify it, which can be used by dictionaries to track unique keys
# and sets to track unique values. This is why Python requires us to use immutable datatypes for the keys in a dictionary.

# The lists used in the code above are NOT immutable, and thus cannot be hashed and used as dictionary keys. Can you try modifying the datatype of the keys in the dictionary
# above to make the code run without errors? Hint: What other data structure can you use to store a sequence of values and is immutable?
