# asyncio - Asynchronous I/O, event loop, coroutines and tasks
# it is used as a foundation for multiple Python asynchronous frameworks that provide high-performance network and web-servers,
#  database connection libraries, distributed task queues, etc.
# asyncio is often a perfect fit for IO-bound and high-level structured network code.

# When you have a long running operation in Python it'll block the main thread.
# This can limit scaling and responsiveness. You can update your code to use async/await to spin off a separate worker!