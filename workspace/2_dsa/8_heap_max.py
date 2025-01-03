# Max Heap
import heapq

a = [-3, 2, 1, 0, 3, 6, 10, 14, 9]
n = len(a)

for i in range(n):
    a[i] = -a[i]

heapq.heapify(a)

print(a) # [-14, -9, -10, -2, -3, -6, -1, 0, 3]

largest = -heapq.heappop(a)

print(largest) # 14

# Insert
heapq.heappush(a, -5) # insert 5 into max heap

print(a) # [-10, -9, -6, -5, -3, 3, -1, 0, -2]

# Build heap from scratch
# Time: O(n log n)

b = [-5, 4, 2, 1, 7, 0, 3]

heap = []

for x in b:
    heapq.heappush(heap, x)
    print(heap, len(heap))

'''
[-5] 1
[-5, 4] 2
[-5, 4, 2] 3
[-5, 1, 2, 4] 4
[-5, 1, 2, 4, 7] 5
[-5, 1, 0, 4, 7, 2] 6
[-5, 1, 0, 4, 7, 2, 3] 7
'''

# Putting tuples of items on the heap

c = [5, 4, 3, 5,4, 3, 5, 4]

from collections import Counter

counter = Counter(c)

print(counter) # Counter({5: 3, 4: 3, 3: 2})

heap = []

for key, value in counter.items():
    heapq.heappush(heap, (value, key))

print(heap) # [(2, 3), (3, 5), (3, 4)]

