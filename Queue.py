import asyncio

price_queue = asyncio.Queue()

# async def mock_ws_producer():
#     for price in [100, 101, 105, 110]:
#         print("WS 수신:", price)
#         await price_queue.put(price)
#         await asyncio.sleep(0.5)

async def strategy_worker():
    while True:
        price = await price_queue.get()
        print("전략 판단:", price)

async def main():
    await asyncio.gather(strategy_worker())


if __name__ == "__main__":
    asyncio.run(main())
