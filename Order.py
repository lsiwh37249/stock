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
from Queue import order_queue, order_worker_queue


class Order:
    def __init__(self):
        self.price_up_ratio_threshold = 0.7
        self.volume_ratio_threshold = 1.5
        self.amount_ratio_threshold = 2
        self.time_window_threshold = 3
        self.cond_index_threshold = True
        
    # 조건 생성
    def make_condition(self, data):
        # data = {
        #    "ticker": parts[1],
        #    "current_price": current_price,
        #    "trade_volume": trade_volume,
        #    "trade_amount": trade_amount,
        #    "acc_volume": acc_volume,
        #    "date": date,
        #    "time": time
        #}
        
        #price_up_ratio = data["current_price"] / data["acc_trade_amount"]
        volume_ratio = data["trade_volume"] / data["acc_volume"]
        amount_ratio = data["trade_amount"] / data["acc_trade_amount"]
        
        conclusion = {
            "volume_ratio": volume_ratio,
            "amount_ratio": amount_ratio
        }        
        return conclusion
    
    def conclusion(self, data):
        condition = self.make_condition(data)
        if (condition["volume_ratio"] >= self.volume_ratio_threshold) + (condition["amount_ratio"] >= self.amount_ratio_threshold) >= 2 : # 2개 중 2개 이상 조건 만족해야 함
            return True
        else:
            return False
    
    def order_conclusion(self, data):
        if self.conclusion(data):
            # 주문서 작성
            order_data = {
                # 시장가 주문문
                "ticker": data["ticker"],
                "price": data["current_price"],
                "quantity": data.get("quantity", data.get("trade_volume", 1)),  # quantity가 없으면 trade_volume 사용
                "is_buy": True
            }
            return order_data
        else:
            # 주문 거절 -> 로그 생성
            
            return {
                "ticker": "",
                "price": "",
                "quantity": "",
                "is_buy": ""
            }
        
    async def order(self):
        while True:
            try:
                data = await order_queue.get()
                order_condition = self.order_conclusion(data)
                print("order_condition: ", order_condition)
                #큐에 전송
                await order_worker_queue.put(order_condition)
            except Exception as e:
                print(f"Order error: {e}")
                import traceback
                traceback.print_exc()