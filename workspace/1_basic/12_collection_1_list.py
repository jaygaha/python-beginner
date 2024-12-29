# collection: single variable that holds multiple values
# list: [] collection which is ordered and changeable. Allows duplicate members.
# set: {} collection which is unordered and unindexed. No duplicate members.
# tuple: () collection which is ordered and unchangeable. Allows duplicate members.

# 1. List

fruits = ["apple", "banana", "cherry"]

print(dir(fruits)) # returns various methods that can be used with list (fruits)

print(fruits) # ['apple', 'banana', 'cherry']
print(fruits[1])  # banana
print(fruits[:1])  # ['apple']
print(fruits[::-1])  # ['cherry', 'banana', 'apple']

for fruit in fruits:
    print(fruit)

# find in collection
print("apple" in fruits)  # True
print("apple" not in fruits)  # False
print("coconut" in fruits)  # False

# add to collection
fruits.append("melon")
print(fruits)  # ['apple', 'banana', 'cherry', 'melon']

fruits.insert(1, "grape")
print(fruits)  # ['apple', 'grape', 'banana', 'cherry', 'melon']

fruits[0] = "orange"

for fruit in fruits:
    print(fruit)

# remove from collection
fruits.remove("banana")
print(fruits)  # ['orange', 'grape', 'cherry', 'melon']

# sort collection
fruits.sort()
print(fruits)  # ['cherry', 'grape', 'melon', 'orange']

# reverse collection
fruits.reverse()
print(fruits)  # ['orange', 'melon', 'grape', 'cherry']

# index of collection
print(fruits.index("melon"))  # 1

# count of collection
fruits.append("grape")
print(fruits.count("grape"))  # 2

# clear collection
fruits.clear()
print(fruits)  # []