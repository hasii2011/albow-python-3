
from functools import total_ordering

from typing import Callable


class ScheduledCall:
    """
    Fixed the

    > TypeError: '<' not supported between instances of 'ScheduledCall' and 'ScheduledCall'

    in `Scheduler.schedule_call`,  by implementing the method '\\_\\_lt\\_\\_()'

    """
    def __init__(self, timeToExecute: float, func: Callable, interval: float):
        """
        Use `albow.core.Scheduler.Scheduler.timestamp` as the `timeToExecute` value

        Args:
            timeToExecute:  When we want this function executed

            func: The function to execute

            interval:  How long to delay after -timeToExecute_ has elapsed
        """
        self.time = timeToExecute
        self.func = func
        self.interval = interval

    def __ne__(self, other):
        return not (self == other)

    def __lt__(self, other):
        return self.time < other.time

    def __eq__(self, theOtherOne):
        """
        Overrides the default implementation
        """
        if isinstance(theOtherOne, ScheduledCall):
            if self.time == theOtherOne.time and \
               self.func == theOtherOne.func and \
               self.interval == theOtherOne.interval:
                return True

        return False

    def __le__(self, other):
        return self.time <= other.time

    def __gt__(self, other):
        return self.time > other.time, other

    def __ge__(self, other):
        return self.time >= other.time, other

    def __str__(self):

        formattedMe:str = f"time: {self.time}, func: {self.func}, interval: {self.interval}"
        return formattedMe
