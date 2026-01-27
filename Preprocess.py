import asyncio
from datetime import datetime

from Queue import preprocess_queue, order_queue

class Preprocess:
    def __init__(self):
        self.UNIT_LEN = 46
        
    def parse_h0stcnt0(self, raw):
        raw = "0|H0STCNT0|004|005930^151938^159200^2^7100^4.67^154694.32^150500^159500^149200^159200^159100^1^26227159^4057189006750^130764^202725^71961^166.35^9445533^15712944^1^0.60^127.55^090024^2^8700^150950^5^-300^090530^2^10000^20260127^20^N^10012^3746^788277^110357^0.44^18627338^140.80^0^^150500^005930^151938^159200^2^7100^4.67^154694.33^150500^159500^149200^159200^159100^78^26227237^4057201424350^130764^202726^71962^166.35^9445533^15713022^1^0.60^127.55^090024^2^8700^150950^5^-300^090530^2^10000^20260127^20^N^10011^3441^788275^110002^0.44^18627338^140.80^0^^150500^005930^151938^159100^2^7000^4.60^154694.33^150500^159500^149200^159200^159100^1^26227238^4057201583450^130765^202726^71961^166.35^9445534^15713022^5^0.60^127.55^090024^2^8600^150950^5^-400^090530^2^9900^20260127^20^N^10011^3441^788275^110002^0.44^18627338^140.80^0^^150500^005930^151938^159200^2^7100^4.67^154694.34^150500^159500^149200^159200^159100^73^26227311^4057213205050^130765^202727^71962^166.35^9445534^15713095^1^0.60^127.55^090024^2^8700^150950^5^-300^090530^2^10000^20260127^20^N^10011^3441^788275^110002^0.44^18627338^140.80^0^^150500"
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
                    "trade_volume": int(fields[base + 12] or 0),
                    "trade_amount": int(fields[base + 2] or 0)
                                     * int(fields[base + 12] or 0),
                    "acc_volume": int(fields[base + 13] or 0),
                    "acc_trade_amount": int(fields[base + 14] or 0),
                }
                datas.append(parsed)

            except IndexError:
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