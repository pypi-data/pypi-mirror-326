
from multiprocessing import Queue


class TqdmMonitor:
    def __init__(self, collector: Queue):
        self._tqdm = None

    def set_tqdm(self, tqdm):
        self._tqdm = tqdm

    def update(self, msg):
        if self._tqdm is not None:
            self._tqdm.write(msg)


    
    def _collect(self) -> list[TqdmSnapshot]:
        '''Collect the current state of all known tqdm instances'''
        bars = []

        self._discover()

        for known_instance in self.raw_tqdm:
            for i in known_instance._instances:  # pylint: disable=protected-access
                snapshot = TqdmSnapshot.from_bar(i)
                logging.info("Snapshotted bar %s" % snapshot)
                bars.append(snapshot)

        return bars

    def _discover(self):
        '''Discover a new tqdm instance and add it to the known instances'''

        for t in self.raw_tqdm:
            for instance in t._instances:  # pylint: disable=protected-access
                if instance not in self.raw_tqdm:
                    self.add(instance)
