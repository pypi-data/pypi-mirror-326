from datetime import datetime
import unittest
from unittest import mock

from tqdmpromproxy.bucket import PrometheusBucket


class TestPrometheusBucket(unittest.TestCase):

    def setUp(self):
        bucket = "test_bucket"
        item_scale = "items"
        retired_attrs = ["completed"]
        current_attrs = ["completed", "rate"]

        self.vanilla_bucket = PrometheusBucket(
            bucket, item_scale, retired_attrs, current_attrs)

    def _create_mock_tqdm(self, name: str):
        instance = mock.Mock()
        instance.identity.return_value = f"new_instance_{name}"

        for attr in self.vanilla_bucket.current_attrs:
            setattr(instance, attr, 2)

        for attr in self.vanilla_bucket.retired_attrs:
            setattr(instance, attr, 1234)

        return instance

    def test_init(self):
        bucket = "test_bucket"
        item_scale = "items"
        retired_attrs = ["completed"]
        current_attrs = ["completed", "rate"]

        prom_bucket = PrometheusBucket(
            bucket, item_scale, retired_attrs, current_attrs)

        self.assertEqual(prom_bucket.bucket, bucket)
        self.assertEqual(prom_bucket.item_scale, item_scale)
        self.assertEqual(prom_bucket.current_attrs, current_attrs)
        self.assertEqual(prom_bucket.retired_attrs, retired_attrs)
        self.assertEqual(prom_bucket.aggregated, {"completed": 0})
        self.assertEqual(prom_bucket.known_instances, {})
        self.assertEqual(prom_bucket.retired_instances, 0)

    def test_matches(self):
        bucket = "test_bucket"
        item_scale = "items"
        retired_attrs = ["completed"]
        current_attrs = ["completed", "rate"]

        prom_bucket = PrometheusBucket(
            bucket, item_scale, retired_attrs, current_attrs)

        matching_instance = mock.Mock()
        matching_instance.bucket.return_value = bucket

        self.assertTrue(prom_bucket.matches(matching_instance))

        different_instance = mock.Mock()
        different_instance.bucket.return_value = "nope"

        self.assertFalse(prom_bucket.matches(different_instance))

    def test_update_single(self):

        new_instance = mock.Mock()
        new_instance.identity.return_value = "new_instance"

        self.assertEqual(len(self.vanilla_bucket.known_instances), 0)

        self.vanilla_bucket.update(new_instance)
        self.vanilla_bucket.update(new_instance)  # do it again

        self.assertTrue(new_instance
                        in self.vanilla_bucket.known_instances)
        self.assertEqual(len(self.vanilla_bucket.known_instances), 1)

    def test_update_multiple(self):

        instances = [self._create_mock_tqdm(i) for i in range(10)]

        self.assertEqual(len(self.vanilla_bucket.known_instances), 0)

        for i in instances:
            self.vanilla_bucket.update(i)

        self.assertEqual(
            len(self.vanilla_bucket.known_instances), len(instances))

    def test_retire(self):

        keep = self._create_mock_tqdm("keep")
        retire = self._create_mock_tqdm("retire")

        instances = [keep, retire]

        for i in instances:
            self.vanilla_bucket.update(i)

        self.vanilla_bucket.retire(retire)

        self.assertEqual(
            len(self.vanilla_bucket.known_instances), 1)
        self.assertEqual(self.vanilla_bucket.retired_instances, 1)

        for attr in self.vanilla_bucket.retired_attrs:
            self.assertEqual(self.vanilla_bucket.aggregated[attr], 1234)

        for attr in self.vanilla_bucket.current_attrs:
            if attr not in self.vanilla_bucket.retired_attrs:
                self.assertFalse(attr in self.vanilla_bucket.aggregated.keys())

    def test_prune(self):
        instances = [self._create_mock_tqdm(i) for i in range(10)]

        for i in instances:
            self.vanilla_bucket.update(i)

        for k in self.vanilla_bucket.known_instances.keys():
            self.vanilla_bucket.known_instances[k] = datetime.fromisoformat(
                "2000-01-01T00:00:00")

        self.vanilla_bucket.prune(1)
        self.assertEqual(
            len(self.vanilla_bucket.known_instances), 0)
        self.assertEqual(self.vanilla_bucket.retired_instances, len(instances))

    def test_export(self):
        instances = [self._create_mock_tqdm(i) for i in range(10)]

        for i in instances:
            self.vanilla_bucket.update(i)

        lines = list(self.vanilla_bucket.to_prometheus_lines())
        real_lines = [line for line in lines if not line.startswith("#")]

        # expect count to be
        # 1x active
        # 1x finished
        # 1x each indified attr
        all_attrs = set(self.vanilla_bucket.current_attrs +
                        self.vanilla_bucket.retired_attrs)
        self.assertEqual(len(real_lines), 2 + len(all_attrs))


if __name__ == '__main__':
    unittest.main()
