# collection: single variable that holds multiple values
# list: [] collection which is ordered and changeable. Allows duplicate members.
# set: {} collection which is unordered and unindexed. No duplicate members.
# tuple: () collection which is ordered and unchangeable. Allows duplicate members.

# 2. Set

fruits = {"apple", "banana", "cherry"}

print(fruits) # random order {'banana', 'apple', 'cherry'}

# print(dir(fruits)) # returns various methods that can be used with set (fruits)

print(len(fruits)) # 3

# index is not supported
# print(fruits[1]) # TypeError: 'set' object is not subscriptable

# # find in collection
print("apple" in fruits)  # True
print("apple" not in fruits)  # False
print("coconut" in fruits)  # False

# add to collection
fruits.add("melon")

print(fruits)  # {'banana', 'apple', 'cherry', 'melon'}


# remove from collection
fruits.remove("banana")

print(fruits)  # {'apple', 'cherry', 'melon'}

# pop from collection
fruits.pop()

print(fruits)  # randomly remove first element {'cherry', 'melon'}

# # clear collection
fruits.clear()
print(fruits)  # []

# No duplicate members
fruits = {"apple", "banana", "cherry", "apple"}

print(fruits)  # {'banana', 'apple', 'cherry'}

