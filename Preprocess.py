import asyncio
from datetime import datetime

from Queue import preprocess_queue, order_queue

class Preprocess:
    def __init__(self):
        self.ticker = None
        self.volume = None
        self.amount = None
        self.settlement_price = None
        self.date = None
        self.time = None


    async def preprocess(self):
        while True:
            raw = await preprocess_queue.get()
    
            self.ticker = 12334
            self.volume = 1000000
            self.amount = 1000000000
            self.settlement_price = 1000
            self.date = datetime.now().strftime("%Y-%m-%d")
            self.time = datetime.now().strftime("%H:%M:%S")
               
            data = {
                "ticker": self.ticker,
                "volume": self.volume,
                "amount": self.amount,
                "settlement_price": self.settlement_price,
                "date": self.date,
                "time": self.time
            }
            
            # TODO: raw 파싱해서 data 채우기 (지금은 더미)
            await order_queue.put(data)
