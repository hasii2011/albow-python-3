
class ScheduledCall:
    """
    Fixed the

    > TypeError: '<' not supported between instances of 'ScheduledCall' and 'ScheduledCall'

    in `Scheduler.schedule_call`,  by implementing the method '\\_\\_lt\\_\\_()'

    """
    def __init__(self, timeParam, func, interval):

        self.time = timeParam
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

