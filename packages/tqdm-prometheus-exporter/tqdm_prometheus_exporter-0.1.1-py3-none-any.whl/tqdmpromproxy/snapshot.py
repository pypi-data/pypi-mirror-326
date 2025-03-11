import datetime
from tqdm import tqdm as native_tqdm


class TqdmSnapshot():
    '''Snapshot of the state of a tqdm instance'''

    def __init__(self,
                 item: native_tqdm,
                 bar_id: int = None,
                 time_ms: datetime.datetime = None,
                 desc: str = None,

                 n: int = None,
                 elapsed: int = None,
                 unit: str = None,
                 prefix: str = None,
                 unit_scale: str = None,
                 rate: float = None,
                 postfix: str = None,
                 unit_divisor: int = None,
                 initial: int = None,
                 total: int = None,
                 **_kwargs
                 ):
        # from our wrapper
        self.bar_id = bar_id
        self.item = item
        self.time_ms = time_ms

        # from tqdm api args
        self.completed = n
        self.total = total
        self.elapsed = elapsed
        self.prefix = prefix
        self.postfix = postfix
        self.unit = unit
        self.unit_scale = unit_scale
        self.unit_divisor = unit_divisor
        self.rate = rate
        self.initial = initial

        # from other/meta attributes
        self.desc = desc

    def __repr__(self):
        friendly = "Instance %s Bar = %s, Finished %s Total %s, throughput %s" % \
            (self.item, self.desc, self.completed, self.total, self.rate)

        # + " [ " + ', '.join(f"{prop}= {self.__getattribute__(prop)}" for prop in dir(self) if not prop.startswith("_")) + "]"
        return friendly

    def identity(self):
        '''Return a unique identifier for this instance.
        These properties should not change during the lifetime of the instance'''
        return str(self.bar_id) + self.prefix

    def bucket(self):
        '''Return a summary of the instance, so like instances can be aggregated
        For example all Gzip tasks, or all FileUpload tasks'''
        return self.prefix[0:self.prefix.find(' ') or 10]

    @classmethod
    def from_bar(cls, bar: native_tqdm):
        if not isinstance(bar, native_tqdm):
            raise ValueError("Expected a tqdm instance")

        return cls(bar,
                   bar_id=getattr(bar, 'pos', 0),
                   desc=getattr(bar, 'desc', ''),
                   time_ms=datetime.datetime.now(),
                   **bar.format_dict)
