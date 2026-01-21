# - price_up_ratio= 상승종목수 / 테마종목수 ≥ 0.6
# - volume_ratio = 현재거래량 / 직전 N분 평균 ≥ 1.5배
# - amount_ratio = 현재거래대금 / 직전 N분 평균 ≥ 2배
# - time_window = 3분, 동시 발생 종목 수(sync_count) ≥5
# - cond_index = (
    #    KOSPI_change > -1.0 and
    #    KOSDAQ_change > -1.0
# )
# 

import asyncio
from Queue import order_queue

class Order:
    def __init__(self):
        self.price_up_ratio = 0.7
        self.volume_ratio = 1.5
        self.amount_ratio = 2
        self.time_window = 3
        self.cond_index = True
        
    def make_condition(self, data):
        # data 기반 조건 생성
        return data
    
    def conclusion(self, data):
        # 판단 후 주문 진행 + 5개 중에 3개를 만족하면 주문 진행
        if self.price_up_ratio >= 0.6 and self.volume_ratio >= 1.5 and self.amount_ratio >= 2 and self.time_window >= 5 and self.cond_index == True:
            return True
        else:
            return False
    
    def order_conclusion(self, data):
        if self.conclusion(data):
            # 주문 진행
            print("주문 진행")
            return True
        else:
            # 주문 거절 -> 로그 생성
            print("주문 거절")
            return False
        
    async def order(self):
        while True:
            data = await order_queue.get()
            order_condition = self.order_conclusion(data)
            print("order_condition: ", order_condition)