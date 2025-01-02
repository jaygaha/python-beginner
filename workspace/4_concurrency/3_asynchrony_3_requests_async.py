# Fetching web pages in async
# it fetches the pages concurrently

import asyncio
import aiohttp
import time

async def fetch_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    page1 = asyncio.create_task(fetch_async("https://jaygaha.com.np"))
    page2 = asyncio.create_task(fetch_async("https://www.google.com"))
    await asyncio.gather(page1, page2)

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    print(f"DONE in {time.time() - start_time} seconds")# DONE in 0.3 seconds