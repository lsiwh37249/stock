import os
import json
import requests
import websocket
import ssl
import asyncio
import random
import time
from Queue import raw_queue, preprocess_queue, order_queue

class Realtime:
    def __init__(self, ticker=None):
        self.APP_KEY = os.environ["REAL_APPKEY"]    
        self.APP_SECRET = os.environ["REAL_APPSECRETKEY"]
        self.ACCESS_TOKEN = None
        self.APPROVAL_KEY = None
        self.WS_URL = "wss://ops.koreainvestment.com:21000"
        self.loop: asyncio.AbstractEventLoop | None = None
        self.ticker = ticker

    def auth(self):
        url = "https://openapi.koreainvestment.com:9443/oauth2/Approval"
        headers = {"content-type": "application/json"}
        body = {
            "appkey": self.APP_KEY,
            "secretkey": self.APP_SECRET
        }

        res = requests.post(url, headers=headers, json=body)
        data = res.json()

        self.APPROVAL_KEY = data["approval_key"]
        return self.APPROVAL_KEY

    def send_to_queue(self, raw):
        """
        websocket-client(동기) 콜백/루프에서 asyncio.Queue로 안전하게 전달.

        - 이벤트 루프가 연결되어 있으면: run_coroutine_threadsafe로 put
        - 아니면(디버그/동기 단독): put_nowait 시도
        """
        if self.loop is not None and self.loop.is_running():
            asyncio.run_coroutine_threadsafe(raw_queue.put(raw), self.loop)
            return
        raw_queue.put_nowait(raw)

    async def ws_client_async(self):
        """
        WebSocket 클라이언트를 별도 스레드에서 실행하는 async 래퍼
        """
        loop = asyncio.get_running_loop()
        
        def _ws_client():
            """동기 WebSocket 클라이언트 (블로킹)"""
            print("WS 연결 시도")

            ws = websocket.WebSocket()
            ws.connect("ws://ops.koreainvestment.com:21000")

            print("WS 연결 성공")

            subscribe_msg = {
                "header": {
                    "approval_key": self.APPROVAL_KEY,
                    "custtype": "P",
                    "tr_type": "1",
                    "content-type": "utf-8"
                },
                "body": {
                    "input": {
                        "tr_id": "H0STCNT0",  # 호가 (바로 데이터 옴)
                        "tr_key": self.ticker
                    }
                }
            }

            ws.send(json.dumps(subscribe_msg))
            print("구독 완료")

            while True:
                raw = ws.recv()
                # 별도 스레드에서 직접 run_coroutine_threadsafe 사용
                asyncio.run_coroutine_threadsafe(preprocess_queue.put(raw), loop)
                

        # 별도 스레드에서 실행
        await loop.run_in_executor(None, _ws_client)

if __name__ == "__main__":
    async def _main():
        r = Realtime(ticker="222080")
        r.loop = asyncio.get_running_loop()
        r.auth()

        await r.ws_client_async()

    asyncio.run(_main())
    