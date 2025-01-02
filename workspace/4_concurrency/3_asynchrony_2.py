import asyncio

async def say_hello_async():
    await asyncio.sleep(2)# simulates waiting for 2 seconds
    print("Hello, async!")

async def do_something_else():
    print("Starting to do something else")
    await asyncio.sleep(1)# simulates waiting for 1 second
    print("Finished another task")

async def main():
    await asyncio.gather(
        say_hello_async(),
        do_something_else()
    )

if __name__ == "__main__":
    asyncio.run(main())

# The output will be:
'''
Starting to do something else
Finished another task
Hello, async!
'''