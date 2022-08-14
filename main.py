import asyncio
import random


async def main():
    for i in range(100):
        asyncio.create_task(load_data(i))
    await asyncio.sleep(3)


async def load_data(i: int):
    sleep_time = random.uniform(0, 2.6)
    await asyncio.sleep(sleep_time)
    print(f"some data {i}, loading time: {sleep_time}")

asyncio.run(main())

