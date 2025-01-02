# Numpy Arrays: a Python package for numerical computing
#   Less Memory
#   Fast
#   Convenient
#
# pip install numpy

import numpy as np
import time
import sys

# single dimensional
a = np.array([1,3,9])

print(a) # [1 3 9]

# Multi dimensional
b = np.array([(1, 2, 3), (4,5,6)], dtype=np.float64)

print(b)
'''
[[1 2 3]
 [4 5 6]]
'''

# list
s = range(1000)
print(sys.getsizeof(5)*len(s)) # 28000

# NumPy
d = np.arange(1000)
print(d.size * d.itemsize) # 8000

size = 1000000

l1 = range(size)
l2 = range(size)
a1 = np.arange(size)
a2 = np.arange(size)

start_time = time.perf_counter()
result = [(i, j) for i, j in zip(l1, l2)]
end_time = time.perf_counter() - start_time
print(f"Time elapsed for the list: {end_time}") # 0.39320869999937713

start_time = time.perf_counter()
result =a1 + a2
end_time = time.perf_counter() - start_time
print(f"Time elapsed for the NumPy array: {end_time}") # 0.1377698999713175

# ndim: find the dimension of the array
print(b.ndim) # 2

# itemsize:  calculate the byte size of each element
print(a.itemsize) # 8 every element occupies 8 byte in the numpy array

# dtype: find data type of a particular element
print(a.dtype) # int64

# size
print(a.size) # 3

# shape
print(b.shape) # (2, 3)

# reshape: when you change the number of rows and columns which gives a new view to an object
c = np.array([(7,8,9), (10,11,12)])
print(c)
'''
[[ 7  8  9]
 [10 11 12]]
'''

c = c.reshape(3,2)
print(c)

'''
[[ 7  8]
 [ 9 10]
 [11 12]]
'''

# TODO: other remaining functions

