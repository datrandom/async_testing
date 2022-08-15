import asyncio
import random
from datetime import datetime


last_response_time = datetime.now()
response_list = []


async def get_data(name: str, current_loop: int):
    global last_response_time
    sleep_time = round(random.uniform(1.9, 3.5), 2)
    await asyncio.sleep(sleep_time)
    print(datetime.now() - last_response_time)
    response_list.append(datetime.now() - last_response_time)
    last_response_time = datetime.now()


async def main():
    task1 = asyncio.create_task(get_data("Task1", 0))
    await asyncio.sleep(1.8)
    task2 = asyncio.create_task(get_data("Task2", 0))

    for loop in range(1, 100):
        await task1
        await asyncio.sleep(0.2)
        task1 = asyncio.create_task(get_data("Task1", loop))
        await task2
        await asyncio.sleep(0.2)
        task2 = asyncio.create_task(get_data("Task2", loop))

if __name__ == "__main__":
    asyncio.run(main())
    summ = datetime.now() - datetime.now()
    for i in response_list:
        summ += i

    print(f"Average waiting for response: {summ/len(response_list)}")

    breakpoint()
