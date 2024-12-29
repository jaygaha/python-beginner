# collection: single variable that holds multiple values
# list: [] collection which is ordered and changeable. Allows duplicate members.
# set: {} collection which is unordered and unindexed. No duplicate members.
# tuple: () collection which is ordered and unchangeable. Allows duplicate members.

# 3. Tuple

fruits = ("apple", "banana", "cherry", "apple")

print(fruits) # ('apple', 'banana', 'cherry', 'apple')

# print(dir(fruits)) # returns various methods that can be used with tuple (fruits)
# print(help(fruits)) # returns various methods that can be used with tuple (fruits)

print(len(fruits)) # 4

# in operatpr to find in collection
print("apple" in fruits)  # True

# index
# print(fruits[1])  # banana
print(fruits.index("banana"))  # 1

# count
print(fruits.count("apple"))  # 2

# iterable

for fruit in fruits:
    print(fruit) # apple, banana, cherry, apple





