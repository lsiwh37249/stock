from pykis import PyKis, KisAuth, KisQuote, KisBalance
from Realtime import Realtime
from Queue import price_queue
import os
import asyncio
class Stock():
    def __init__(self):
        # 실전투자용 PyKis 객체를 생성합니다.
        self.kis = PyKis("secret.json", keep_token=True)
        self.kis = PyKis(KisAuth.load("secret.json"), keep_token=True)
        
        # 모의투자용 PyKis 객체를 생성합니다.
        #self.kis = PyKis("secret.json", "virtual_secret.json", keep_token=True)
        #self.kis = PyKis(KisAuth.load("secret.json"), KisAuth.load("virtual_secret.json"), keep_token=True)

    # 시세 조회 
    def quote(self):
        stock = self.kis.stock("AAPL")
        quote: KisQuote = stock.quote()
        print(quote)

    def account(self):
        account = self.kis.account()
        balance: KisBalance = account.balance()
        print(repr(balance))
    
    async def real_time_quote(self):
        while True:
            tick = await price_queue.get()
            print(f"[STOCK] Queue → 전략: {tick}")

    def order(self):
        pass

    def main(self):
        print("=== 시세 조회 ===")
        self.quote()
        
        print("\n=== 계좌 조회 ===")
        #self.account()
    
# main
if __name__ == "__main__":
    s = Stock()
