from threading import Thread
from bottle import WSGIRefServer, run, route
from bottle import route, run, response, Bottle
from queue import Empty, Queue
from concurrent.futures import Future, ThreadPoolExecutor
import requests

import logging


class AsyncMetricServer:
    def __init__(self, queue: Queue, address: str="localhost", port: int=9000):
        self.address = address
        self.port = port

        self.snapshot: str = "# HELP No metric data has been collected yet. Check back soon\n"

        global TQDM_PROM_DATA
        TQDM_PROM_DATA = self.snapshot

        self.bottle = Bottle()
        self.bottle.route('/metrics')(self.metrics)

        self.queue = queue
        self.poller = ThreadPoolExecutor(max_workers=1)
        self.wsgi = None

        self.wsgi = WSGIRefServer(
            app=self.bottle, host=self.address, port=self.port)
        self.server = Thread(
            target=self.wsgi.run, args=(self.bottle, ), daemon=True)

        self._stop = False
        self.additional_content: str = ''

    def start(self):
        self.poller.submit(self.poll)
        self.server.start()

    def stop(self):
        self._stop = True
        
        if not hasattr(self.wsgi, 'srv'):
            # dirty force lazy load
            try:
                requests.get(f'http://{self.address}:{self.port}/shutdown', timeout=0.1)
            except requests.exceptions.ConnectTimeout:
                pass
            finally:
                pass

        if hasattr(self.wsgi, 'srv'):
            self.wsgi.srv.shutdown()
        self.server.join()

    def poll(self):
        last_found = 0
        while not self._stop:
            while not self.queue.empty():
                try:

                    item = self.queue.get(0.1)
                    self.snapshot = item
                    last_found = 0
                    logging.info("Polled queue")
                except Empty:
                    last_found += 1

                    if last_found % 10 == 0:
                        logging.info("No new items found in queue")

                finally:
                    pass

    @route('/metrics')
    def metrics(self):
        response.content_type = 'application/text; charset=utf-8'
        logging.info("Metrics requested, returning %d bytes" %
                     len(self.snapshot))
        return self.snapshot
