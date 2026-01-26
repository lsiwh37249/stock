import asyncio
from datetime import datetime

from Queue import preprocess_queue, order_queue

class Preprocess:

    def parse_h0stcnt0(self, raw: str) -> dict:
        """
        H0STCNT0 실시간 체결 데이터 파서
        - 현재가격
        - 체결량
        - 체결 거래대금 (price * volume)
        - 누적 거래량
        - 누적 거래대금
        """
        try:
            # JSON 형식 (구독 성공 응답 등)은 스킵
            if raw.strip().startswith("{"):
                return None
            
            # 파이프(|) 형식만 처리
            parts = raw.split("|")
            if len(parts) < 4 or parts[1] != "H0STCNT0":
                return None  # H0STCNT0 데이터가 아니거나 형식이 맞지 않음

            data = parts[3].split("^")
            
            # 데이터 필드가 충분한지 확인
            if len(data) < 14:
                print(f"Insufficient data fields: {len(data)}")
                return None

            current_price = int(data[2])
            trade_volume = int(data[3])
            acc_volume = int(data[12])
            acc_trade_amount = int(data[13])

            trade_amount = current_price * trade_volume  # 🔥 체결 거래대금

            date = datetime.now().strftime("%Y-%m-%d")
            time = datetime.now().strftime("%H:%M:%S")

            # parts[3]의 첫 번째 요소가 종목코드 (예: "018880")
            ticker_code = data[0] if len(data) > 0 else ""
            
            parsed_data = {
                "ticker": ticker_code,
                "current_price": current_price,
                "trade_volume": trade_volume,
                "trade_amount": trade_amount,
                "acc_volume": acc_volume,
                "acc_trade_amount": acc_trade_amount,
                "date": date,
                "time": time,
            }
            return parsed_data

        except Exception as e:
            print("parse error:", e)
            return None

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
