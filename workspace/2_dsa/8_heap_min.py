# Heaps: helps to quickly retrieve objects with the smallest or the largest key
# A tree-based data structure in which the value of a parent node is ordered in a certain way with respect to the value of its child node(s)
# data structure to manage information


# Build Min Heap (Heapify)
# Time: O(n), Space: O(1)

a = [-3, 2, 1, 0, 3, 6, 10, 14, 9]

import heapq

heapq.heapify(a)

print(a) # [-3, 0, 1, 2, 3, 6, 10, 14, 9]


# Heap Push (Insert element)
# Time O(log n)

heapq.heappush(a, 3)

print(a) # [-3, 0, 1, 2, 3, 6, 10, 14, 9, 3]

# Heap Pop (Extract min)
# Time o(log n)

minn = heapq.heappop(a)

print(a, minn) # [0, 2, 1, 3, 3, 6, 10, 14, 9] -3

# Heap Sort
# time: o(n, log n), Space: o(n)
# Note: o(1) space is possible via swapping, but this is complex

def heapsort(arr):
    heapq.heapify(arr)
    n = len(arr)
    new_list = [0] * n

    for i in range(n):
        minn = heapq.heappop(arr)
        new_list[i] = minn

    return new_list

b = [1, 3, 5, 7, 9, 2, 4, 6, 8, 0]
print()
print(heapsort(b)) # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# Heap Push Pop
# Time: O(lon n)

heapq.heappushpop(a, 88)

# poput 0 and push it 88
print(a) # [1, 2, 6, 3, 3, 88, 10, 14, 9]

# Peak at Min: time: O(1)
print(a[0]) # 1