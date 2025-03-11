

# capture tqdm updates via a process queue
# capture additional argments (network queue length, job queue length)
# expose a prometheus endpoint
# will possibly need to age tqdm as we wont get notified when they are 'done'

from concurrent.futures import ThreadPoolExecutor
from io import StringIO
import logging
from multiprocessing import Queue
from time import sleep

from tqdm import tqdm as native_tqdm

from tqdmpromproxy.bucket import PrometheusBucket
from tqdmpromproxy.metric_server import AsyncMetricServer
from tqdmpromproxy.snapshot import TqdmSnapshot


class TqdmPrometheusProxy():
    def __init__(self, http_host='localhost', http_port=9000, dump_files=0):
        '''
        Start a proxy
        dump_files = 0: no dump, 1= all, 2= all + iteration count 
        '''
        self.tqdm_events = Queue()
        self.tqdm_state = {}  # kv of tqdm_id:state
        self.tqdm_last_update = {}  # kv of tqdm_id:time
        self.http_port = http_port
        self.http_host = http_host
        self.raw_tqdm: list = []  # list of tqdm instances

        self.queue_handler = ThreadPoolExecutor(max_workers=1)
        self.http_handler = ThreadPoolExecutor(max_workers=1)
        self.http_server = AsyncMetricServer(self.tqdm_events, self.http_host, self.http_port)

        self.monitors = [] 

        # sliced stats
        self.buckets: list[PrometheusBucket] = []
        self.dump_files = dump_files

    def tqdm(self, *args, **kwargs):
        instance = native_tqdm(*args, **kwargs)

        self.raw_tqdm += instance

        return instance

    def add(self, tqdm):
        self.raw_tqdm.append(tqdm)

    def remove(self, tqdm):
        self.raw_tqdm.remove(tqdm)

    def start(self):
        self.queue_handler.submit(self._poll)
        self.http_server.start()
        self.http_handler.submit(self.http_server)

    def _start_http_server(self):
        self.http_server.start()

    def __getattr__(self, name):
        return getattr(self.tqdm, name)

    def _poll(self):
        cycle = 0
        while not self.queue_handler._shutdown:
            logging.info("Polling %d instances" % len(self.raw_tqdm))

            try:
                now = self._collect()
                for item in now:
                    matched = False

                    for b in self.buckets:
                        if b.matches(item):
                            b.update(item)
                            matched = True
                            break

                    if not matched:
                        self.buckets.append(
                            PrometheusBucket.from_instance(item))

                logging.info("Polling collected")

            except KeyboardInterrupt:
                logging.info("Polling interrupted")
                break

            except Exception as e:
                logging.error("Error polling instances: %s" %
                              e, exc_info=True)

            finally:
                logging.info("Polling complete")
                sleep(0.3)

            buf = StringIO()
            self._dump_to_stream(buf)
            self.tqdm_events.put(buf.getvalue())

            if self.dump_files > 1:
                with open(f"data/metrics_all.txt", "wt", encoding="utf-8") as f:
                    self._dump_to_stream(f)

                if self.dump_files > 2:
                    with open(f"data/metrics.{str(cycle)}.txt", "wt", encoding="utf-8") as f:
                        self._dump_to_stream(f)
                    

            cycle += 1
            if cycle % 1000 == 0:
                for b in self.buckets:
                    b.prune(1)

    def _dump_to_stream(self, f):
    
        for b in self.buckets:

            for line in b.to_prometheus_lines():
                f.write(line)
                f.write("\n")

    def stop(self):
        self.queue_handler.shutdown()
        self.http_server.stop()
