
from dataclasses import dataclass

@dataclass
class EventLoopParams:

    use_sleep: bool
    relative_pause: bool
    do_draw: bool
    relative_warmup: int