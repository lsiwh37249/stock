import asyncio

from Queue import strategy_worker
from Realtime import Realtime


async def main():
    # consumer 먼저 실행
    consumer = asyncio.create_task(strategy_worker())

    # producer(mock) 실행
    await Realtime.websocket_receiver("000660")

    # 남은 데이터 처리 시간 조금 주고 종료
    await asyncio.sleep(0.2)
    consumer.cancel()


if __name__ == "__main__":
    asyncio.run(main())

