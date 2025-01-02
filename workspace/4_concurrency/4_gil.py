# GIL: a mechanism used in CPython to ensure that only one thread executes Python bytecode at a time.

# reference counting works
import sys
a = []
b = a
print(sys.getrefcount(a)) # 3

# Single thread
import time
from threading import Thread

count = 1000000

def countdown(n):
    while n > 0:
        n -= 1

start = time.time()
countdown(count)
end = time.time()

print(f"Time taken in seconds for single thread: {end - start}") # 0.1050s

# Multi-threading

t1 = Thread(target=countdown, args=(count//2,))
t2 = Thread(target=countdown, args=(count//2,))

start = time.perf_counter()
t1.start()
t2.start()

t1.join()
t2.join()

end = time.perf_counter()-start

print(f"Time taken in seconds for multi-threading: {end}") # 0.1099s