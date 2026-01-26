import asyncio
from datetime import datetime

from Queue import preprocess_queue, order_queue

class Preprocess:

    def parse_h0stcnt0(self, raw: str):
        if raw.strip().startswith("{"):
            return

        parts = raw.split("|")
        if len(parts) < 4 or parts[1] != "H0STCNT0":
            return

        loop = int(parts[2])

        for i in range(loop):
            data = parts[3 + i].split("^")

            try:
                ticker_code = data[0]
                current_price = int(data[2])
                trade_volume = int(data[3])
                acc_volume = int(data[12])
                acc_trade_amount = int(data[13])

                trade_amount = current_price * trade_volume

                now = datetime.now()

                parsed_data = {
                    "ticker": ticker_code,
                    "current_price": current_price,
                    "trade_volume": trade_volume,
                    "trade_amount": trade_amount,
                    "acc_volume": acc_volume,
                    "acc_trade_amount": acc_trade_amount,
                    "date": now.strftime("%Y-%m-%d"),
                    "time": now.strftime("%H:%M:%S"),
                }

                # 🔥 여기서 queue로 넘김
                preprocess_queue.put_nowait(parsed_data)

            except (IndexError, ValueError) as e:
                print("parse error:", e)


    async def preprocess(self):
        print("Preprocess started - waiting for data...")
        while True:
            raw = await preprocess_queue.get()
            print("raw: ", raw)
            data = self.parse_h0stcnt0(raw)
            print("data: ", data)
            if data is not None:  # 파싱 성공한 경우만 큐에 추가
                print(f"✓ Parsed - ticker: {data.get('ticker')}, price: {data.get('current_price')}, volume: {data.get('trade_volume')}")
                await order_queue.put(data)
            else:
                print("Parse failed, skipping...")
