
from dataclasses import dataclass

@dataclass
class EventLoopParams:

    in_relative_mode: bool
    use_sleep: bool
    defer_drawing: bool
    relative_pause: bool
    do_draw: bool
    relative_warmup: int