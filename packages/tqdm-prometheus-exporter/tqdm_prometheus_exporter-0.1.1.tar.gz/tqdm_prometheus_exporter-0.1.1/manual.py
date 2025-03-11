import logging
from multiprocessing import RLock, freeze_support
from time import sleep

from tqdm import tqdm as native_tqdm

from tqdmpromproxy import TqdmPrometheusProxy
from tqdmpromproxy.internal.creator import create_threadpool,queue_tasks

proxy = TqdmPrometheusProxy()

def main():
    # muliprocessing setup
    freeze_support()  # for Windows support
    native_tqdm.set_lock(RLock())  # for managing output contention
    
    proxy.start()
    proxy.add(native_tqdm())

    threads = 3
    depth = 10
    pool = create_threadpool(threads, base=3) # use slots 3, 4, 5
    queue_tasks(pool, threads * depth)

    try:
        for _ in native_tqdm(range(10), desc="Main Loop", position=0):
            for _ in native_tqdm(range(5), desc="Sub Loop", position=1, leave=False):
                for _ in native_tqdm(range(5), desc="Innnnner Loop", position=2, leave=False):
                    sleep(0.2)

    finally:
        proxy.stop()


if __name__ == "__main__":
    logging.basicConfig(filename="data/proxy.log",
                        filemode='w',
                        format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG
                        )
    main()
