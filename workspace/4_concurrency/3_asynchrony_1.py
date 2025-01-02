# asyncio - Asynchronous I/O, event loop, coroutines and tasks
# it is used as a foundation for multiple Python asynchronous frameworks that provide high-performance network and web-servers,
#  database connection libraries, distributed task queues, etc.
# asyncio is often a perfect fit for IO-bound and high-level structured network code.

# When you have a long running operation in Python it'll block the main thread.
# This can limit scaling and responsiveness. You can update your code to use async/await to spin off a separate worker!

import asyncio

async def count():
    print("One")
    # await pauses the execution of the coroutine until the passed coroutine is done
    await asyncio.sleep(1)
    print("Two")

async def main():
    # gather() is used to run multiple coroutines concurrently
    await asyncio.gather(count(), count(), count())

if __name__ == "__main__":
    import time

    # time.perf_counter() returns the current time in seconds
    s = time.perf_counter()

    # run the main coroutine
    asyncio.run(main())

    elapsed = time.perf_counter() - s
    print(f"executed in {elapsed:0.2f} seconds.")
