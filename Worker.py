from pykis import KisStock, KisOrder
from Queue import order_worker_queue

class Worker:
    def __init__(self):
        self.kis = ""

    def sell_worker(self, ticker, pri, quan):
        # REST API 호출
        stock: KisStock = self.kis.stock(ticker) 
        #order: KisOrder = stock.sell(qty=quan)
        print("주문 완료")

    def buy_worker(self, ticker, pri, quan):
        # REST API 호출
        stock: KisStock = self.kis.stock(ticker) 
        #order: KisOrder = stock.buy(qty=quan)
        print("주문 완료")

    async def get_order(self):
        while True:
            order_data = await order_worker_queue.get()
            print("order_data: ", order_data)
            if order_data["is_buy"] == True:
                self.buy_worker(order_data["ticker"], order_data["price"], order_data["quantity"])
            elif order_data["is_buy"] == False:
                self.sell_worker(order_data["ticker"], order_data["price"], order_data["quantity"])
            else:
                print("주문 조건 불만족")


if __name__ == "__main__":
    worker = Worker()
    worker.worker()