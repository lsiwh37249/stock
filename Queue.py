import asyncio

raw_queue = asyncio.Queue()

preprocess_queue = asyncio.Queue()

order_queue = asyncio.Queue()

order_worker_queue = asyncio.Queue()

front_queue = asyncio.Queue()