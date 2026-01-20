import asyncio

price_queue = asyncio.Queue()

async def price_collector():
    while True:
        price = await get_realtime_price()  # WebSocket callback
        await price_queue.put(price)

async def strategy_worker():
    while True:
        price = await price_queue.get()
        print("전략 판단:", price)

async def main():
    await asyncio.gather(
        price_collector(),
        strategy_worker(),
    )

asyncio.run(main())
