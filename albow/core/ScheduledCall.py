
from typing import Callable


class ScheduledCall:
    """
    Fixed the

    > TypeError: '<' not supported between instances of 'ScheduledCall' and 'ScheduledCall'

    in `Scheduler.schedule_call`,  by implementing the method '\\_\\_lt\\_\\_()'

    """
    def __init__(self, timeToExecute: float, func: Callable, interval: float):
        """
        Use `albow.core.Scheduler.timestamp` as the `timeToExecute` value

        Args:
            timeToExecute:  When we want this function executed

            func: The function to execute

            interval:  How long to delay after -timeToExecute_ has elapsed
        """
        self.time = timeToExecute
        self.func = func
        self.interval = interval

    def __lt__(self, other):
        return self.__cmp__(other)

    def __cmp__(self, other):
        #
        # Python 3 update;  cmp is gone
        # https://docs.python.org/3.0/whatsnew/3.0.html#ordering-comparisons
        #
        a = self.time
        b = other.time

        # return cmp(self.time, other.time)
        return (a > b) - (a < b)

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

    def __str__(self):
        formattedObj = "time: {}, func: {}, interval: {}"

        return formattedObj.format(self.time, self.func, self.interval)
