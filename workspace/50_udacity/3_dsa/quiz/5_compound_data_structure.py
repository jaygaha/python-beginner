# Compound data structure
# A compound data structure is a data structure that contains other data structures. For example, a list is a compound data structure because it contains other data structures, such as integers.
# A list is a compound data structure because it contains other data structures, such as integers.


elements = {"hydrogen": {"number": 1,
                         "weight": 1.00794,
                         "symbol": "H"},
              "helium": {"number": 2,
                         "weight": 4.002602,
                         "symbol": "He"}
}
helium = elements["helium"]  # get the helium dictionary
hydrogen_weight = elements["hydrogen"]["weight"]  # get hydrogen's weight

oxygen = {"number":8,"weight":15.999,"symbol":"O"}  # create a new oxygen dictionary
elements["oxygen"] = oxygen  # assign 'oxygen' as a key to the elements dictionary
print('elements = ', elements)

# Adding Values to Nested Dictionaries
#
elements = {'hydrogen': {'number': 1, 'weight': 1.00794, 'symbol': 'H'},
            'helium': {'number': 2, 'weight': 4.002602, 'symbol': 'He'}}

# todo: Add an 'is_noble_gas' entry to the hydrogen and helium dictionaries
# hint: helium is a noble gas, hydrogen isn't
elements['helium']['is_noble_gas'] = True
elements['hydrogen']['is_noble_gas'] = False

# Collections: When we have a group of data we can think about it as a collection (of data elements).
# Example: A list of integers, a tuple of strings, a set of floats, etc.

collections = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
collections = tuple(collections)
collections = set(collections)

collections = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
collections = tuple(collections)
collections = set(collections)
print(collections)

collections = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
print(len(collections))

collections = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for element in collections:
    print(element)

for element in collections:
    print(element)
    print("I'm in a loop")
    print(element)
