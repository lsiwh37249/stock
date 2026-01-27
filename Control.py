import asyncio
from KisAuth import KisAuth
from Realtime import Realtime
from Stock import Stock
from Queue import raw_queue, preprocess_queue, order_queue
from Preprocess import Preprocess
from Order import Order
from Worker import Worker
from Monitor import Monitor
# 수집 -> 테마주 판단 -> 진입 -> 익절/손절 -> 로그 생성 코드 

def create_instance():
    kis_auth = KisAuth()
    stock = Stock()
    realtime = Realtime()
    preproc = Preprocess()
    order = Order()
    worker = Worker()
    monitor = Monitor()
    return kis_auth, stock, realtime, preproc, order, worker, monitor

async def quote(realtime, stock, ticker, preproc, order,worker, monitor):
    # Producer와 Consumer 동시에 실행
    await asyncio.gather(
        realtime.ws_client_async(),  # async 래퍼 사용
        preproc.preprocess(),
        order.order(),
        worker.get_order(),
        #monitor.monitor()
    )

async def main():
    # 클래스 인스턴스 생성성
    kis_auth, stock, realtime, preproc, order, worker, monitor = create_instance()
    worker.kis = kis_auth.main()
    # KisAuth 인증
    kis = kis_auth.main()
    
    # Realtime 인증
    realtime.loop = asyncio.get_running_loop()
    realtime.auth()
    
    # 실시간 시세 조회
    ticker = "005930"
    realtime.ticker = ticker
    
    await quote(realtime, stock, ticker, preproc, order, worker, monitor)

if __name__ == "__main__":
    asyncio.run(main())