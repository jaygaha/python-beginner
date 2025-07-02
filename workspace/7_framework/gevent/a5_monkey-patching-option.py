# --- Best Practice: Perform patching at the very top ---
from gevent import monkey
import gevent
import time
import threading
from typing import List

# It's recommended to patch all but a few modules for simplicity.
# This is the most common use case for selective patching.
print("✅ Patching all modules EXCEPT 'thread' and 'sys'...")
monkey.patch_all(thread=False, sys=False)

def check_patching_status():
    """Checks and prints the status of key modules."""
    print("\n--- Patching Status ---")
    print(f"Socket module patched: {monkey.is_module_patched('socket')}")
    print(f"Time module patched: {monkey.is_module_patched('time')}")
    print(f"Threading module patched: {monkey.is_module_patched('thread')} (Intentionally False)")
    print("-----------------------\n")

def demonstrate_mixed_threading():
    """
    Shows why you might avoid patching 'threading'.

    This allows real OS threads to run alongside gevent greenlets, which can
    be useful for CPU-bound tasks or integrating with libraries that rely on
    native threads.
    """
    print("🚀 Demonstrating mixed gevent greenlets and real OS threads...")
    start_time = time.time()

    def greenlet_task(task_name: str):
        """A non-blocking task for greenlets."""
        print(f"  🟢 Greenlet {task_name}: Starting.")
        # gevent.sleep is cooperative and allows other greenlets to run.
        gevent.sleep(1)
        print(f"  🟢 Greenlet {task_name}: Finished.")

    def native_thread_task(task_name: str):
        """A blocking task that runs in its own OS thread."""
        print(f"  🧵 Native Thread {task_name}: Starting (will block for 2s).")
        # Since 'time' is patched, gevent would normally manage this sleep.
        # However, because it's in a real thread that gevent doesn't manage,
        # it blocks only this thread, not the main gevent loop.
        time.sleep(2)
        print(f"  🧵 Native Thread {task_name}: Finished.")

    # Spawn greenlets that will run concurrently
    greenlets: List[gevent.Greenlet] = [
        gevent.spawn(greenlet_task, f"G{i+1}") for i in range(2)
    ]

    # Start a real OS thread
    native_thread = threading.Thread(target=native_thread_task, args=("T1",))
    native_thread.start()

    # Wait for the greenlets to finish (they will finish in ~1 second)
    gevent.joinall(greenlets)
    print("✅ All greenlets have completed.")

    # Wait for the real thread to finish
    native_thread.join()
    print("✅ Native thread has completed.")

    total_time = time.time() - start_time
    print(f"\n✨ Mixed threading example finished in {total_time:.2f} seconds.")
    print("(Note: Total time is ~2s, dominated by the longest blocking task.)")


if __name__ == "__main__":
    check_patching_status()
    demonstrate_mixed_threading()
