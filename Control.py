import asyncio
from Realtime import Realtime
from Stock import Stock

async def main():
    # 클래스 인스턴스 생성
    realtime = Realtime()
    realtime.loop = asyncio.get_running_loop()
    realtime.auth()
    stock = Stock()

    # Producer와 Consumer 동시에 실행
    await asyncio.gather(
        realtime.ws_client_async("000660"),  # async 래퍼 사용
        stock.real_time_quote()
    )

if __name__ == "__main__":
    asyncio.run(main())