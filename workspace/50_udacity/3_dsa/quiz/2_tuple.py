# 2 Tuples
#
# 1. Tuples are immutable
# 2. Tuples are ordered
# 3. Tuples are indexed
# 4. Tuples are not hashable
# 5. Tuples are not iterable



angkor_wat = (13.4125, 103.866667)

print(type(angkor_wat))
# <class 'tuple'="">

print("AngkorWat is at latitude: {}".format(angkor_wat[0]))
# AngkorWat is at latitude: 13.4125

print("AngkorWat is at longitude: {}".format(angkor_wat[1]))
# AngkorWat is at longitude: 103.866667

# Tuple unpacking
latitude, longitude = angkor_wat
print("AngkorWat is at latitude: {}".format(latitude))
# AngkorWat is at latitude: 13.4125

print("AngkorWat is at longitude: {}".format(longitude))
# AngkorWat is at longitude: 103.866667
#

# What would the output of the following code be? (Treat the comma in the multiple choice answers as newlines.)
tuple_a = 1, 2
tuple_b = (1, 2)

print(tuple_a == tuple_b)
print(tuple_a[1])
