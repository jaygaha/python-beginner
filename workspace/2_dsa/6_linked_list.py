# Linked List: Linked lists are an ordered collection of objects.
# Linked lists differ from lists in the way that they store elements in memory.
# While lists use a contiguous memory block to store references to their data, linked lists store references as part of their own elements.
#
# node -> each element of a linked list
#   Data -> contains the value to be stored in the node
#   Next -> contains a reference to the next node on the list

# collections.deque
# deque (pronounced “deck”), which stands for double-ended queue.

from collections import deque

# empty linked list
# print(deque()) # deque([])

# iterable

print(deque([1, 2, 3])) # deque([1, 2, 3])
print(deque('abc')) # deque(['a', 'b', 'c'])
print(deque([{'data': 'a'}, {'data': 'b'}])) # deque([{'data': 'a'}, {'data': 'b'}])

llist = deque('abcd')
print(llist) # deque(['a', 'b', 'c', 'd'])

# append right side
llist.append('e')
print(llist) # deque(['a', 'b', 'c', 'd', 'e'])

# remove right side
llist.pop()
print(llist) # deque(['a', 'b', 'c', 'd'])

# append left side
llist.appendleft('z')
print(llist) # deque(['z', 'a', 'b', 'c', 'd'])

# remove left side
llist.popleft()
print(llist) # deque(['a', 'b', 'c', 'd'])

# Queues: queues are FIFO
print()

# Example: Busy restaurant; fully packed
# initialize empty
queue = deque()

# Add guests to the queue; waiting list
queue.append('John')
queue.append('Jone')
queue.append('Marry')

print(queue) # deque(['John', 'Jone', 'Marry'])

# As time goes by tables become available; so remove the guest from the list (FIFO)

queue.popleft() # assign seat
print(queue) # deque(['Jone', 'Marry'])

queue.popleft() # assign seat
print(queue) # deque(['Marry'])

queue.popleft() # assign seat
print(queue) # deque()

# Stacks: Uses LIFO

print()

# Example: web browser's history
# map behavior into a stack
history = deque()
base_url = 'https://roadmap.sh/'

# track user behavior
history.appendleft(base_url)
history.appendleft(base_url + 'roadmaps')
history.appendleft(base_url + 'backend')
history.appendleft(base_url + 'backend/projects')

print(history) # deque(['https://roadmap.sh/backend/projects', 'https://roadmap.sh/backend', 'https://roadmap.sh/roadmaps', 'https://roadmap.sh/'])

# Now go back to roadmaps to read other roadmaps
history.popleft()
print(history) # deque(['https://roadmap.sh/backend', 'https://roadmap.sh/roadmaps', 'https://roadmap.sh/'])

history.popleft()
print(history) # deque(['https://roadmap.sh/roadmaps', 'https://roadmap.sh/'])

history.popleft()
print(history) # deque(['https://roadmap.sh/'])

