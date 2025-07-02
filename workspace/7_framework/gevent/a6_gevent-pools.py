import random
import time
from typing import Iterator, List

import gevent
from gevent.pool import Group, Pool

# --- Task Definitions ---

def worker_task(task_id: int, duration: float | None = None) -> str:
    """A worker task that simulates I/O by sleeping for a given duration."""
    if duration is None:
        duration = random.uniform(0.5, 2.0)

    print(f"  Task {task_id}: Starting (will run for {duration:.1f}s)")
    gevent.sleep(duration)
    print(f"  Task {task_id}: Completed")
    return f"Result from task {task_id}"

def risky_task(task_id: int) -> str:
    """A task that systematically fails to demonstrate error handling."""
    gevent.sleep(0.5)
    if task_id % 3 == 0:  # Every 3rd task fails
        print(f"  Task {task_id}: 💥 Failing intentionally!")
        raise ValueError(f"Task {task_id} failed")
    return f"Success from task {task_id}"

# --- Demonstration Functions ---

def demonstrate_pool_concurrency():
    """Shows how a Pool limits concurrency to a fixed size."""
    print("--- 🚀 1 Pool Example: Limited Concurrency ---")

    # A Pool ensures that no more than 3 greenlets run at once.
    pool = Pool(size=3)
    start_time = time.time()

    # The greenlets are spawned but will only start executing as slots in the pool become free.
    greenlets = [pool.spawn(worker_task, i) for i in range(1, 11)]

    pool.join()  # Wait for all spawned greenlets to complete.

    end_time = time.time()
    print(f"\nPool execution finished in {end_time - start_time:.2f} seconds.")
    print(f"Pool size: {pool.size}, Greenlets processed: {len(greenlets)}")

def demonstrate_group_unlimited():
    """Shows how a Group runs all greenlets concurrently without limits."""
    print("\n--- 🚀 2 Group Example: Unlimited Concurrency ---")

    group = Group()
    start_time = time.time()

    # All tasks are spawned and run at once.
    for i in range(1, 6):
        group.spawn(worker_task, i, duration=2)

    group.join()

    end_time = time.time()
    print(f"\nGroup execution finished in {end_time - start_time:.2f} seconds.")
    print(f"(Time is ~2s because all tasks ran in parallel).")

def demonstrate_pool_map():
    """Demonstrates Pool.map to apply a function to a list and get results at the end."""
    print("\n--- 🚀 3 Pool.map Example: Batch Processing ---")

    pool = Pool(size=4)
    inputs = list(range(10))
    start_time = time.time()

    # .map blocks until all results are computed, then returns them in order.
    results: List[int] = pool.map(lambda n: n * n, inputs)

    end_time = time.time()
    print(f"Map finished in {end_time - start_time:.2f} seconds.")
    print(f"Inputs:  {inputs}")
    print(f"Results: {results}")

def demonstrate_pool_imap():
    """Demonstrates Pool.imap to process results as they complete."""
    print("\n--- 🚀 4 Pool.imap Example: Iterative Processing ---")

    pool = Pool(size=3)
    items = ['A', 'B', 'C', 'D', 'E', 'F']
    start_time = time.time()

    # .imap returns an iterator. We get results as soon as they are ready.
    # The order of results corresponds to the order of inputs.
    results_iterator: Iterator[str] = pool.imap(lambda i: f"Processed-{i}", items)

    print("Processing results as they arrive...")
    for result in results_iterator:
        print(f"  -> Received: {result}")

    end_time = time.time()
    print(f"imap finished in {end_time - start_time:.2f} seconds.")

def demonstrate_pool_exceptions():
    """Shows how to check for exceptions in greenlets managed by a Pool."""
    print("\n--- 🚀 5 Pool Exception Handling ---")

    pool = Pool(size=3)

    # Spawn tasks, some of which are designed to fail.
    greenlets = [pool.spawn(risky_task, i) for i in range(1, 8)]
    pool.join() # Wait for all to finish, whether they succeed or fail.

    print("\nChecking results:")
    for g in greenlets:
        if g.successful():
            print(f"  ✅ Success: {g.value}")
        else:
            # g.exception holds the exception object.
            print(f"  ❌ Failed:  {g.exception}")

if __name__ == "__main__":
    demonstrate_pool_concurrency()
    demonstrate_group_unlimited()
    demonstrate_pool_map()
    demonstrate_pool_imap()
    demonstrate_pool_exceptions()
