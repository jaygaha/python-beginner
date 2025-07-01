import gevent


# --- Task Definitions ---

def long_running_task(seconds=5):
    """A sample task that simulates work by sleeping."""
    print(f"  -> Starting long_running_task for {seconds} seconds.")
    for i in range(seconds):
        print(f"  ...working step {i + 1}/{seconds}")
        gevent.sleep(1)
    result = f"Task finished after {seconds} seconds."
    print(f"  -> {result}")
    return result

def task_with_exception():
    """A sample task that is designed to fail."""
    print("  -> Starting task_with_exception.")
    gevent.sleep(1)
    print("  -> Task raising ValueError!")
    raise ValueError("This is a simulated failure.")

# --- Demonstration Functions ---

def demonstrate_lifecycle():
    """Demonstrates the basic lifecycle and state of a successful greenlet."""
    print("\n--- Demonstrating Basic Greenlet Lifecycle ---")

    # gevent.spawn() starts the greenlet immediately
    g = gevent.spawn(long_running_task, 3)

    print(f"[Initial State] Greenlet running: {g!r}")
    print(f"[Initial State] Is ready? {g.ready()}") # False, it's still running
    print(f"[Initial State] Is successful? {g.successful()}") # False, not finished yet

    # .join() waits for the greenlet to complete its execution
    print("Waiting for greenlet to complete with join()...")
    g.join()

    print("\nGreenlet has completed.")
    print(f"[Final State] Is dead? {g.dead}") # True, it has stopped
    print(f"[Final State] Is ready? {g.ready()}") # True, result is available
    print(f"[Final State] Was successful? {g.successful()}") # True, no exceptions
    print(f"[Final State] Value: {g.value!r}") # Access the return value
    print(f"[Final State] Exception: {g.exception}") # None, as it was successful

def demonstrate_kill():
    """Demonstrates forcefully terminating a greenlet with kill()."""
    print("\n--- Demonstrating Greenlet Termination with kill() ---")

    g = gevent.spawn(long_running_task, 10) # Start a long task

    print(f"[Initial State] Greenlet running: {g!r}")

    # Allow the greenlet to run for a few seconds
    print("Allowing greenlet to run for 3 seconds...")
    gevent.sleep(3)

    print("\nKilling the greenlet now...")
    # .kill() raises a GreenletExit exception inside the greenlet
    g.kill()

    # You might need a small sleep to allow the hub to process the kill
    gevent.sleep(0)

    print("\nGreenlet has been killed.")
    print(f"[Final State] Is dead? {g.dead}") # True
    print(f"[Final State] Is ready? {g.ready()}") # True, because it's stopped
    print(f"[Final State] Was successful? {g.successful()}") # False, it was killed
    print(f"[Final State] Value: {g.value!r}") # None
    print(f"[Final State] Exception: {type(g.exception)}") # GreenletExit

def demonstrate_exception_handling():
    """Demonstrates how to handle greenlets that raise exceptions."""
    print("\n--- Demonstrating Greenlet Exception Handling ---")

    g = gevent.spawn(task_with_exception)

    print(f"[Initial State] Greenlet running: {g!r}")

    # It's often best to join() and then check for the exception.
    # The exception is contained within the greenlet and doesn't crash the main program.
    print("Waiting for greenlet to complete with join()...")
    g.join()

    print("\nGreenlet has completed.")
    print(f"[Final State] Is dead? {g.dead}") # True
    print(f"[Final State] Is ready? {g.ready()}") # True
    print(f"[Final State] Was successful? {g.successful()}") # False
    print(f"[Final State] Value: {g.value!r}") # None

    # You can now safely inspect the exception object
    print(f"[Final State] Exception Type: {type(g.exception)}")
    print(f"[Final State] Exception Value: {g.exception}")

    # If you .get() a failed greenlet, it will re-raise the exception
    try:
        g.get()
    except ValueError as e:
        print(f"\nCaught exception with g.get(): {e!r}")


if __name__ == "__main__":
    demonstrate_lifecycle()
    demonstrate_kill()
    demonstrate_exception_handling()
