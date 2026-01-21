import asyncio
from KisAuth import KisAuth
from Realtime import Realtime
from Stock import Stock
from Queue import raw_queue, preprocess_queue, order_queue
from Preprocess import Preprocess
from Order import Order
# 수집 -> 테마주 판단 -> 진입 -> 익절/손절 -> 로그 생성 코드 

def create_instance():
    kis_auth = KisAuth()
    stock = Stock()
    realtime = Realtime()
    preproc = Preprocess()
    order = Order()
    return kis_auth, stock, realtime, preproc, order

async def quote(realtime, stock, stock_code, preproc, order):
    # Producer와 Consumer 동시에 실행
    await asyncio.gather(
        realtime.ws_client_async(stock_code),  # async 래퍼 사용
        stock.real_time_quote(),
        preproc.preprocess(),
        order.order()
    )

async def main():
    # 클래스 인스턴스 생성성
    kis_auth, stock, realtime, preproc, order = create_instance()

    # KisAuth 인증
    kis = kis_auth.main()
    
    # Realtime 인증
    realtime.loop = asyncio.get_running_loop()
    realtime.auth()
    
    # 실시간 시세 조회
    stock_code = "032820"
    
    await quote(realtime, stock, stock_code, preproc, order)


if __name__ == "__main__":
    asyncio.run(main())