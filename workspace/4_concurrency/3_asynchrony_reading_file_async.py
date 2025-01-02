# Asynchrony: Reading file asynchronously
# pip install --upgrade pip aiofiles asyncio

import asyncio
import aiofiles
import time

async def read_file_async(file_path):
    async with aiofiles.open(file_path, 'r') as file:
        return await file.read()

async def read_all_async(file_paths):
    tasks = [read_file_async(file_path) for file_path in file_paths]
    # *tasks: Unpacks the list of tasks
    return await asyncio.gather(*tasks)

# Running the async function
async def main():
    file_paths = ['workspace/4_concurrency/output1.txt', 'workspace/4_concurrency/output2.txt', 'workspace/4_concurrency/output3.txt']

    # start time
    start_time = time.perf_counter()

    data = await read_all_async(file_paths)

    # end time
    end_time = time.perf_counter() - start_time

    print(data)
    print()
    print(f"executed in {end_time:0.2f} seconds.")

if __name__ == '__main__':
    asyncio.run(main())

# Output:
'''
['This is text 1', 'This is text 2', 'This is text 3']

executed in 0.02 seconds.
'''
