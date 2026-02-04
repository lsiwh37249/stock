from Queue import raw_queue, preprocess_queue, order_queue, order_worker_queue, front_queue
import asyncio
from datetime import datetime


def write_log(lines: str):
    with open("monitor.log", "a") as f:
        f.write(lines)
        f.flush()

class Monitor:
    async def monitor(self):
        loop = asyncio.get_running_loop()

        try:
            while True:
                log = (
                    f"[{datetime.now()}]\n"
                    f"raw_queue size: {raw_queue.qsize()}\n"
                    f"preprocess_queue size: {preprocess_queue.qsize()}\n"
                    f"order_queue size: {order_queue.qsize()}\n"
                    f"order_worker_queue size: {order_worker_queue.qsize()}\n"
                    f"front_queue size: {front_queue.qsize()}\n"
                    + "-" * 30 + "\n"
                )

                await loop.run_in_executor(None, write_log, log)

                await asyncio.sleep(1)

        except asyncio.CancelledError:
            print("monitor task cancelled gracefully")
            raise
