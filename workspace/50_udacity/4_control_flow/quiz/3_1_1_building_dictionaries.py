# Building Dictionaries
# A dictionary is a mutable data type that stores mappings of unique keys to values. Here's a dictionary that stores elements and their atomic numbers.
# elements = {"hydrogen": 1, "helium": 2, "carbon": 6}
# print(elements)

# Method 1 for loop

book_title =  ['great', 'expectations','the', 'adventures', 'of', 'sherlock','holmes','the','great','gasby','hamlet','adventures','of','huckleberry','fin']

# count word count
# use a dictionary to store the count of each word
word_count = {}

for word in book_title:
    if word in word_count:
        word_count[word] += 1
    else:
        word_count[word] = 1

print(word_count)

# Method using the get method

word_count = {}

for word in book_title:
    word_count[word] = word_count.get(word, 0) + 1

print(word_count)
print()

# Iterating Through Dictionaries with For Loops
cast = {
           "Jerry Seinfeld": "Jerry Seinfeld",
           "Julia Louis-Dreyfus": "Elaine Benes",
           "Jason Alexander": "George Costanza",
           "Michael Richards": "Cosmo Kramer"
       }

print("Iterating through keys:")
for key in cast:
    print(key)

print("\nIterating through keys and values:")

for key, value in cast.items():
    print("Actor: {}    Role: {}".format(key, value))

# Quiz: Fruit Basket with Dictionaries

# You would like to count the number of fruits in your basket.
# In order to do this, you have the following dictionary and list of
# fruits.  Use the dictionary and list to count the total number
# of fruits, but you do not want to count the other items in your basket.

result = 0
basket_items = {'pears': 5, 'grapes': 19, 'kites': 3, 'sandwiches': 8, 'bananas': 4}
fruits = ['apples', 'oranges', 'pears', 'peaches', 'grapes', 'bananas']

#Iterate through the dictionary
for fruit in fruits:
    if fruit in basket_items:
        result += basket_items[fruit]

print(result)

# Task 2": 2nd method: with any dictionary and list the above solution can be used
print()
#Example 1

result = 0
basket_items = {'pears': 5, 'grapes': 19, 'kites': 3, 'sandwiches': 8, 'bananas': 4}
fruits = ['apples', 'oranges', 'pears', 'peaches', 'grapes', 'bananas']

# Your previous solution here
for fruit in fruits:
    if fruit in basket_items:
        result += basket_items[fruit]

print(result)

#Example 2

result = 0
basket_items = {'peaches': 5, 'lettuce': 2, 'kites': 3, 'sandwiches': 8, 'pears': 4}
fruits = ['apples', 'oranges', 'pears', 'peaches', 'grapes', 'bananas']

# Your previous solution here
for fruit in fruits:
    if fruit in basket_items:
        result += basket_items[fruit]

print(result)


#Example 3

result = 0
basket_items = {'lettuce': 2, 'kites': 3, 'sandwiches': 8, 'pears': 4, 'bears': 10}
fruits = ['apples', 'oranges', 'pears', 'peaches', 'grapes', 'bananas']

# Your previous solution here
for fruit in fruits:
    if fruit in basket_items:
        result += basket_items[fruit]

print(result)

print()

# You would like to count the number of fruits in your basket.
# In order to do this, you have the following dictionary and list of
# fruits.  Use the dictionary and list to count the total number
# of fruits and not_fruits.

fruit_count, not_fruit_count = 0, 0
basket_items = {'apples': 4, 'oranges': 19, 'kites': 3, 'sandwiches': 8}
fruits = ['apples', 'oranges', 'pears', 'peaches', 'grapes', 'bananas']

#Iterate through the dictionary
for key, value in basket_items.items():
    if key in fruits:
        fruit_count = fruit_count + value
    else:
        not_fruit_count = not_fruit_count + value

print(fruit_count, not_fruit_count)

# for fruit in fruits:
#     #if the key is in the list of fruits, add to fruit_count.
#     if fruit in basket_items:
#         fruit_count += basket_items[fruit]
#     #if the key is not in the list, then add to the not_fruit_count
#     else:
#         not_fruit_count += basket_items[fruit]


# print(fruit_count, not_fruit_count)
