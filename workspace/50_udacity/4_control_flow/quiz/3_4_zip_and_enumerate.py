# Zip and Enumerate
# Zip: returns an iterator of tuples, where the i-th tuple contains the i-th element from each of the argument sequences or iterables.
# Enumerate: returns an iterator of tuples, where the i-th tuple contains the i-th element from the iterable and its index.

letters = ['a', 'b', 'c']
nums = [1, 2, 3]

for letter, num in zip(letters, nums):
    print("{}: {}".format(letter, num))

some_list = [('a', 1), ('b', 2), ('c', 3)]
letters, nums = zip(*some_list)

print(letters)
print(nums)

# enumerate
letters = ['a', 'b', 'c', 'd', 'e']

for i, letter in enumerate(letters):
    print(i, letter)


# Quiz: Zip Coordinates
x_coord = [23, 53, 2, -12, 95, 103, 14, -5]
y_coord = [677, 233, 405, 433, 905, 376, 432, 445]
z_coord = [4, 16, -6, -42, 3, -6, 23, -1]
labels = ["F", "J", "A", "Q", "Y", "B", "W", "X"]

points = []
# write your for loop here

# Use zip to iterate over the coordinates and labels
for point, x, y, z in zip(labels, x_coord, y_coord, z_coord):
    # Create the formatted string and append it to the points list
    points.append("{}: {}, {}, {}".format(*point))


for point in points:
    print(point)

# Quiz: Zip Lists to a Dictionary
cast_names = ["Barney", "Robin", "Ted", "Lily", "Marshall"]
cast_heights = [72, 68, 72, 66, 76]

cast =  cast = dict(zip(cast_names, cast_heights)) # replace with your code
print(cast)

# Quiz: Unzip Tuples
# Unzip the cast tuple into two names and heights tuples.
cast = (("Barney", 72), ("Robin", 68), ("Ted", 72), ("Lily", 66), ("Marshall", 76))

# define names and heights here
names, heights = zip(*cast)

print(names)
print(heights)

# Quiz: Transpose with Zip
data = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11))

data_transpose = tuple(zip(*data))
print(data_transpose)

# Quiz: Enumerate
cast = ["Barney Stinson", "Robin Scherbatsky", "Ted Mosby", "Lily Aldrin", "Marshall Eriksen"]
heights = [72, 68, 72, 66, 76]

# write your for loop here
for index, name in enumerate(cast):
    # cast[index] = f"{name} {heights[index]}"
    cast[index] = name + " " + str(heights[index])

print(cast)