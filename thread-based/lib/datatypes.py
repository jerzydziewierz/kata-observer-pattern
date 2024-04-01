from attr import dataclass, field
import time

@dataclass
class Config:
    name: str = "unset"
    verbosity: int = 0

    def __post_init__(self):
        self.name = "unset"
        self.verbosity = 0


@dataclass
class SomeData:
    timestamp: float = field(factory=time.time, repr=False, eq=False, order=False, hash=False)
    source: str = field(default="unset", repr=False, eq=False, order=False, hash=False)
    value: int = field(default=0)

