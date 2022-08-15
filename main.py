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
    a = 0
    for _ in range(50):
        a += 1
        task1 = asyncio.create_task(get_data("Task1", a))
        await asyncio.sleep(2)
        task2 = asyncio.create_task(get_data("Task2", a))
        await task1

if __name__ == "__main__":
    asyncio.run(main())
    summ = datetime.now() - datetime.now()
    for i in response_list:
        summ += i

    print(f"Average waiting for response: {summ/len(response_list)}")

    breakpoint()
