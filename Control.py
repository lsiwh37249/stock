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

async def run_task(name, coro):
    while True:
        try:
            await coro()
        except Exception as e:
            import logging
            logger = logging.getLogger(name)
            logger.exception(f"Error in {name}: {e}")
            await asyncio.sleep(1)

async def quote(realtime, stock, ticker, preproc, order,worker, monitor):
    # Producer와 Consumer 동시에 실행
    await asyncio.gather(
        run_task("realtime", realtime.ws_client_async),  # async 래퍼 사용
        run_task("preproc", preproc.preprocess),
        run_task("order", order.order),
        run_task("worker", worker.get_order),
        run_task("monitor", monitor.monitor)
    )

async def main():
    # 클래스 인스턴스 생성성
    kis_auth, stock, realtime, preproc, order, worker, monitor = create_instance()
    worker.kis = kis_auth.main()
    # KisAuth 인증
    kis = kis_auth.main()
    
    # Realtime 인증
    #realtime.loop = asyncio.get_running_loop()
    realtime.auth()
    
    # 실시간 시세 조회
    # 삼성전자 주식 코드
    # 네이버 주식 코드
    ticker = "005930"
    #ticker = "035720"
    realtime.ticker = ticker
    
    await quote(realtime, stock, ticker, preproc, order, worker, monitor)

if __name__ == "__main__":
    asyncio.run(main())