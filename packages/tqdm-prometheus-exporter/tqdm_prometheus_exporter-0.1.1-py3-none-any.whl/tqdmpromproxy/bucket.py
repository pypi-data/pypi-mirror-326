
from datetime import datetime
import logging

from tqdmpromproxy.snapshot import TqdmSnapshot


class PrometheusBucket:
    '''
    Collection of all grouped metrics'''

    def __init__(self, bucket: str, item_scale: str, retired_attrs: list[str], current_attrs: list[str]):
        self.bucket = bucket
        self.item_scale = item_scale
        self.current_attrs = list.copy(current_attrs)
        self.retired_attrs = list.copy(retired_attrs)

        self.aggregated = dict([(attr, 0) for attr in self.retired_attrs])

        self.known_instances = {}
        self.retired_instances = 0

    def matches(self, instance: TqdmSnapshot):
        return instance.bucket() == self.bucket

    def update(self, instance: TqdmSnapshot):
        if instance.identity() not in [i.identity() for i in self.known_instances]:
            self.known_instances[instance] = 0

        self.known_instances[instance] = datetime.now()

    # pylint: disable=unnecessary-dunder-call
    def to_prometheus_lines(self):
        '''Return the metrics as a prometheus string'''
        yield f"# TQDM group {self.bucket} "
        yield f"{self.bucket}_active_count {len(self.known_instances)}"
        yield f"{self.bucket}_finished_count {self.retired_instances}"

        yield f"## Individual properties with scale {self.item_scale}"
        for prop in self.current_attrs:

            val = sum([instance.__getattribute__(prop) or 0
                      for instance in self.known_instances.keys()])

            if prop in self.retired_attrs:
                val += self.aggregated[prop]

            yield f"{self.bucket}_{prop}_{self.item_scale} {val}"

    # pylint: disable=unnecessary-dunder-call
    def retire(self, instance: TqdmSnapshot):
        '''Move an instance from the active to the retired list'''
        if instance.identity() in [i.identity() for i in self.known_instances]:
            for prop in self.retired_attrs:
                self.aggregated[prop] += instance.__getattribute__(prop)

            del self.known_instances[instance]

            self.retired_instances += 1

    def prune(self, max_age: int):
        '''Remove any instances that are no longer active'''
        to_remove = []
        for key, value in self.known_instances.items():
            if (datetime.now() - value).total_seconds() > max_age:
                to_remove.append(key)

        for key in to_remove:
            self.retire(key)

    @classmethod
    def from_instance(cls, snapshot: TqdmSnapshot):
        return cls(snapshot.bucket(), snapshot.unit, ['completed'], ['completed', 'rate'])
