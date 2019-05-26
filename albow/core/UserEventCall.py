
from typing import Callable

from dataclasses import dataclass


@dataclass
class UserEventCall:

    func: Callable
    userEvent: int
