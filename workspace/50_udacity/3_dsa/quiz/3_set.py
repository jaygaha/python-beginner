# 3 Sets
#
# 1. Sets are unordered
# 2. Sets are not hashable
# 3. Sets are not iterable
# 4. Sets are mutable
# 5. Sets doesnot contain duplicate elements

continents = {"Asia", "Africa", "North America", "South America", "Antarctica"}
print(len(continents))
# 5
#
# get third element from the set
print('North America' in continents)
#
# Set: a collection of unique items
continent_set = set(continents)

print('Asia' in continents)
print('Asia' in continent_set)

# Add a new continent to the set
continent_set.add("Europe")

# Pop() removes and returns an arbitrary element from the set
europe = continent_set.pop()
print(europe)

# What would the output of the following code be?

a = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
b = set(a)
print(b)
print(len(a) - len(b))

a = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
b = set(a)
b.add(5)
b.pop()
