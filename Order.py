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
        self.volume_ratio_threshold = 1
        self.amount_ratio_threshold = 0
        self.time_window_threshold = 0
        self.cond_index_threshold = True
        self.prev_volumes = []
        self.prev_amounts = []
        
    # 조건 생성
    def make_condition(self, data):
        current_volume = data["trade_volume"]
        
        # 이전 평균 거래량 계산 (최근 5틱)
        if len(self.prev_volumes) >= 5:
            avg_prev_volume = sum(self.prev_volumes[-5:]) / 5
        else:
            avg_prev_volume = max(1, sum(self.prev_volumes) / max(1, len(self.prev_volumes)))
        
        # 거래량 급등 판단
        volume_ratio = current_volume / avg_prev_volume
        
        self.prev_volumes.append(current_volume)

        conclusion = {
            "volume_ratio": volume_ratio,
            #"amount_ratio": amount_ratio
        }        
        return conclusion
    
    def conclusion(self, data):
        condition = self.make_condition(data)
        if (condition["volume_ratio"] >= self.volume_ratio_threshold): 
            return True
        else:
            return False
    
    def order_conclusion(self, data):
        if self.conclusion(data):
            # 주문서 작성
            order_data = {
                # 시장가 주문
                "ticker": data["ticker"],
                "price": data["current_price"],
                "quantity": data.get("quantity", 1),  # quantity가 없으면 trade_volume 사용
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
                # 주문 조건 만족할 때만 worker 큐에 넣음 (불만족 시 큐에 쌓이지 않음)
                if order_condition.get("ticker"):
                    print("order_condition: ", order_condition)
                    await order_worker_queue.put(order_condition)
                else:
                    print("주문 조건 불만족, 스킵")
            except Exception as e:
                print(f"Order error: {e}")
                import traceback
                traceback.print_exc()