# use a multiprocessing approach where you use multiple processess instead of threads
# each Python process gets its own Python interpreter and memory space so the GIL won't be a problem
from multiprocessing import Pool
import time

count = 1000000

def countdown(n):
    while n > 0:
        n -= 1

def main():
    pool = Pool(processes=2)
    start_time = time.perf_counter()

    r1 = pool.apply_async(countdown, [count//2])
    r2 = pool.apply_async(countdown, [count//2])
    pool.close()
    pool.join()

    end_time = time.perf_counter() - start_time

    print(f"Time taken in seconds for multi-processing: {end_time}") # 0.0570s

if __name__ == "__main__":
    main()