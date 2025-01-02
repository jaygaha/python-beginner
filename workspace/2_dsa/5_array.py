# Array: It is a collection of elements of the same data type and size.
# Array is a fixed size data structure which means once we define the size of the array, we cannot change it.

import array as arr

# Create an array
# Syntax: array(data_type, [elements])
# i - integer, f - float, d - double, c - character, b - byte, u - unicode character
intgr = arr.array('i', [1, 2, 3, 4, 5, 6])
print(intgr) # Output: array('i', [1, 2, 3, 4, 5, 6])
print(intgr[0]) # Output: 1

#
digts = arr.array('d', [1.1, 2.2, 3.3, 4.4, 5.5])

print(digts) # Output: array('d', [1.1, 2.2, 3.3, 4.4, 5.5])
print(digts[1]) # Output: 2.2

# Find the length of an array
print(len(intgr)) # Output: 6
print(len(digts)) # Output: 5

# Append an element to an array
# useful when we want to add a single element to the array
intgr.append(7)
print(intgr) # Output: array('i', [1, 2, 3, 4, 5, 6, 7])

# Extend an array
# useful when we want to add multiple elements to the array
intgr.extend([8, 9, 10])
print(intgr) # Output: array('i', [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

# Insert an element to an array
# useful when we want to add an element at a specific index
digts.insert(1, 6.6)
print(digts) # Output: array('d', [1.1, 6.6, 2.2, 3.3, 4.4, 5.5])

# array concatenation
digts2 = arr.array('d', [7.7, 8.8, 9.9])
digts3 = arr.array('d') # empty array

digts3 = digts + digts2
print(f"Combined array: {digts3}") # Output: array('d', [1.1, 6.6, 2.2, 3.3, 4.4, 5.5, 7.7, 8.8, 9.9])

# Remove an element from an array

# pop() - removes the element at the specified index and returns it
# without an index, it removes the last element
print(intgr.pop()) # Output: 10
print(intgr.pop(4)) # Output: 6

print(intgr) # Output: array('i', [1, 2, 3, 4, 6, 7, 8, 9])

# remove() - removes the first occurrence of the specified element
intgr.remove(4)
print(intgr) # Output: array('i', [1, 2, 3, 6, 7, 8, 9])

# slice an array
# useful when we want to extract a sub-array from the original array
# Syntax: array[start:stop:step]
print(intgr[1:5]) # Output: array('i', [2, 3, 6, 7])

# loop through an array
print("Loop through an array")
for x in digts3:
    print(x)

# specific index
print("Specific index")
for x in digts3[1:5]:
    print(x)

# clear an array
# useful when we want to remove all elements from the array
intgr.clear()
print(intgr) # Output: array('i')
