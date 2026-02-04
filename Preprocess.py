import asyncio
from datetime import datetime

from Queue import preprocess_queue, order_queue

class Preprocess:
    def __init__(self):
        self.UNIT_LEN = 46
        
    def parse_h0stcnt0(self, raw):
        # JSON 응답(구독 성공 등)은 파이프 형식이 아니므로 스킵
        if "{" in raw:
            return None

        parts = raw.split("|")

        loop = int(parts[2])

        fields = parts[3].split("^")  # 빈 필드 유지

        datas = []

        for i in range(loop):
            base = i * self.UNIT_LEN

            try:
                parsed = {
                    "ticker": fields[base + 0],
                    "current_price": int(fields[base + 2] or 0),
                    "trade_volume": int(fields[base + 12] or 0), #량
                    "trade_amount": int(fields[base + 2] or 0) #대금
                                     * int(fields[base + 12] or 0),
                    "acc_volume": int(fields[base + 13] or 0),
                    "acc_trade_amount": int(fields[base + 14] or 0),
                }
                datas.append(parsed)

            except Exception as e:
                print(f"Preprocess error: {e}")
                import traceback
                traceback.print_exc()
                # 필드 자체가 부족한 경우
                continue

        return datas

    async def preprocess(self):
        print("Preprocess started - waiting for data...")
        while True:
            raw = await preprocess_queue.get()
            print("raw: ", raw)
            datas = self.parse_h0stcnt0(raw)
            print("datas: ", datas)
            if datas is not None:
                print("datas is not None")
                for data in datas:
                    await order_queue.put(data)
            else:   
                print("datas is None")