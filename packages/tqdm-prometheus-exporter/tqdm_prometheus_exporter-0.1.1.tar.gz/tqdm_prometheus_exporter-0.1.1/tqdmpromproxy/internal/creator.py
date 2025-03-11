from multiprocessing import Queue
import traceback
from tqdm import tqdm 
from time import sleep

from tqdmpromproxy.internal.executor import TaskCountingPoolExecutor

def generator_init(lock, queue):
    tqdm.set_lock(lock)

    global tqdm_slot
    # if this fails the queue is empty and we should exit
    tqdm_slot = queue.get(timeout=1)

def create_threadpool(size:int=2, base: int = 0):
        offsets = Queue()

        for r in range(base, base+size):
            offsets.put(r)

        pool = TaskCountingPoolExecutor(size,
                                    initializer=generator_init,
                                    initargs=(tqdm.get_lock(), offsets))
    
        return pool


def queue_tasks(pool, quanity:int):
    names = ["Upload", "Download", "Gzip", "Bzip", "Tar", "Untar", "Copy", "Move", "Delete", "List"]
    try:
        for q in range(quanity):
           pool.submit(_off_thread_task, (names[q % len(names)]))
    except Exception as e:
        print(e)
        traceback.print_exc()
        pool.shutdown(wait=True)


def _off_thread_task(name:str, duration:int = 5, step:float = 0.2):
    
    with tqdm(total=duration, desc=name, position=tqdm_slot, leave=False) as pbar:
        for _ in range(int(duration / step)):
            sleep(step)
            pbar.update(step)