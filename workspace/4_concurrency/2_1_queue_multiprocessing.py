# Python multiprocessing Queue class
# The Queue class is used to share data between processes.
# It is a FIFO (First In First Out) data structure.

from multiprocessing import Queue

genres = ["Action", "Adventure", "Comedy", "Drama", "Fantasy", "Horror", "Mystery", "Romance", "Thriller", "Western"]
count = 1

# create a queue
queue = Queue()

print("Put items in the queue")
for genre in genres:
    queue.put(genre)
    print(f"Item {count} added to the queue: {genre}")
    count += 1

print("\nGet items from the queue")
count = 0
while not queue.empty():
    print(f"Item {count} removed from the queue: {queue.get()}")
    count += 1