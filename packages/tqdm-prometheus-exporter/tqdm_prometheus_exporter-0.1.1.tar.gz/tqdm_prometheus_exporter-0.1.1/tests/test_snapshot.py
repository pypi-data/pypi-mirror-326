import datetime
import time
import unittest

from tqdm import tqdm as native_tqdm

from tqdmpromproxy.snapshot import TqdmSnapshot


class TestSnapshot(unittest.TestCase):

    def delaybody(self, seconds=0.1):
        time.sleep(seconds)

    def generate_bytes(self, kbytes):
        for _ in range(kbytes):
            yield b" " * 1024

    def test_manual(self):
        snapshot_time = datetime.datetime.now()
        snapshot = TqdmSnapshot(
            item=None,
            total=100,
            desc="Test Bar",
            n=50,
            time_ms=snapshot_time,
            unit="foo",
            bar_id=1
        )

        self.assertIsNone(snapshot.item)
        self.assertEqual(snapshot.total, 100)
        # self.assertEqual(snapshot.desc, "Test Bar")
        self.assertEqual(snapshot.completed, 50)
        self.assertEqual(snapshot.time_ms, snapshot_time)
        self.assertEqual(snapshot.bar_id, 1)
        self.assertEqual(snapshot.unit, "foo")
        self.assertIsNotNone(repr(snapshot))

    def test_from_bar_range(self):
        bar = native_tqdm(range(101), desc="Test Bar")
        bar.update(23)

        snapshot = TqdmSnapshot.from_bar(bar)

        self.assertEqual(snapshot.item, bar)
        self.assertEqual(snapshot.total, 101)
        self.assertEqual(snapshot.desc, "Test Bar")
        self.assertEqual(snapshot.completed, 23)
        self.assertIsNotNone(snapshot.time_ms)
        self.assertEqual(snapshot.bar_id, 0)

    def test_from_noiterator(self):
        bar = native_tqdm(desc="Checking prerequsites",
                          bar_format='{desc}', position=12, leave=False, unit="seconds waited")
        bar.update(23)

        snapshot = TqdmSnapshot.from_bar(bar)

        self.assertEqual(snapshot.item, bar)
        self.assertIsNone(snapshot.total)
        self.assertEqual(snapshot.desc, "Checking prerequsites")
        self.assertEqual(snapshot.completed, 23)
        self.assertIsNotNone(snapshot.time_ms)
        self.assertEqual(snapshot.bar_id, -12)

    def test_from_generator(self):
        keys = ["first", "second", "third", "fourth", "fifth"]
        values = [1, 2, 3, 4, 5]

        tuples = zip(keys, values)

        snaps = []
        for f, sz in (pbar := native_tqdm(tuples, desc="Task", unit='files', position=1, leave=False)):
            snaps.append((TqdmSnapshot.from_bar(pbar), f, sz))
            self.delaybody()

        counter = 0
        for snap, f, sz in snaps:
            self.assertEqual(snap.total, None)
            self.assertEqual(snap.desc, "Task")
            self.assertEqual(snap.completed, counter, f"Iteration {
                             counter} got {snap.completed}")
            self.assertEqual(snap.bar_id, -1)
            self.assertEqual(snap.unit, "files")

            print(f"Snap {snap} {f} {sz}")

            counter += 1

    def test_bytes(self):
        snaps = []
        target = 5 * 1024**3  # 1GB

        step_values = [0, 1, 2, 3, 4]
        units = ['B', 'B', 'KB', 'MB', 'GB']

        limit = len(step_values)-1

        steps = 3  # multiplies major unit to b make a number 'enough'

        with native_tqdm(self.generate_bytes(1), desc="byte(scale) through",
                         total=target,
                         unit='B', unit_scale=True) as pbar:

            for offset in range(limit):
                pbar.update(steps * 1024**step_values[offset])
                self.delaybody()
                snaps.append(TqdmSnapshot.from_bar(pbar))

                print(pbar)

        counter = 0
        running_total = 0
        for snap in snaps:
            self.assertEqual(snap.total, target)
            running_total += steps * 1024**counter
            self.assertEqual(snap.completed, running_total, f"Iteration {
                             counter} got {snap.completed}")
            # self.assertEqual(snap.unit, units[counter], f"Iteration {
            #                  counter} wanted {units[counter]} got {snap.unit}. possible (total so far {running_total})")

            print(f"Snap {snap} ")

            counter += 1
