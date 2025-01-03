# Queue: Operations are performed FIFO (first in, first out),
#  which means that the first element added will be the first one removed.
# A queue can be implemented using an array.

from collections import deque

q = deque()

print(q) # deque([])

# Enqueue - add element to the right - O(1)
q.append(5)
q.append(6)

print(q) # deque([5, 6])

# Dequeue (pop left) - remove element from the left - O(1)
q.popleft()

print(q) # deque([6])

# Peek from left side - O(1)
q[0] # 6

# Peek fom right side (last) O(1)
q[-1] # 6