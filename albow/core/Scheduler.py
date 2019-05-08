import logging

from time import time

from bisect import insort

from pygame.locals import USEREVENT

from pygame.event import Event

from albow.core.CoreUtilities import add_modifiers
from albow.core.CoreUtilities import  time_base

from albow.core.ScheduledCall import ScheduledCall


class Scheduler:

    ourLogger = logging.getLogger(__name__)

    ourScheduledCalls = []

    """
    A static class to avoid using module functions
    """
    @staticmethod
    def schedule(delay, func):
        """
        .. WARNING::
            Deprecated, use `schedule_call` or `schedule_event` instead.

        """
        Scheduler.schedule_call(delay * 1000.0, func)

    @staticmethod
    def schedule_call(delay, func, repeat=False):
        """
        Arrange for the given function to be called after the specified
        delay in milliseconds. Scheduled functions are called synchronously from
        the event loop, and only when the frame timer is running. If repeat is
        true, call will be made repeatedly at the specified interval, otherwise
        it will only be made once.

        Args:
            delay:  The scheduled delay in milliseconds

            func:  The function to call

            repeat: Set to _True_ to repeat, else _False_

        Returns:   Returns a token that can be passed to `Scheduler.cancel_ call()`.

        """
        t = Scheduler.timestamp() + delay
        if repeat:
            r = delay
        else:
            r = 0.0
        item = ScheduledCall(t, func, r)
        insort(Scheduler.ourScheduledCalls, item)
        return item

    @staticmethod
    def schedule_event(delay, func, repeat=False):
        """
        Like `Scheduler.schedule_call` except that the function is passed an event containing the current timestamp and
        the state of the modifier keys.

        Args:
            delay:  The scheduled delay in milliseconds

            func:  The function to call

            repeat: Set to _True_ to repeat, else _False_
        """
        def thunk():
            # TODO:  Fix to include the time attribute
            #
            # Pygame 1.9 update
            #
            # event = Event(USEREVENT, time = timestamp())
            event = Event(USEREVENT, dict=None)
            add_modifiers(event)
            func(event)

        Scheduler.schedule_call(delay, thunk, repeat)

    @staticmethod
    def timestamp():
        return time() * 1000.0 - time_base

    @staticmethod
    def cancel_call(token):
        """
        Cancel a previously scheduled call, given a token returned by
        `Scheduler.schedule_call` or `Scheduler.schedule_event`.

        Args:
            token:  The token that represents the call to cancel

        """
        try:
            Scheduler.ourScheduledCalls.remove(token)
        except ValueError as ve:
            # pass
            Scheduler.ourLogger.error("Cancel call exception: %s", ve)

    @staticmethod
    def make_scheduled_calls():
        #  Legacy
        sched = Scheduler.ourScheduledCalls
        t = Scheduler.timestamp()
        while sched and sched[0][0] <= t:
            sched[0][1]()
            sched.pop(0)

    @staticmethod
    def make_due_calls(time_now, until_time):
        """
        Call all functions scheduled at or before time_now.

        Args:
            time_now:  When to make the call

            until_time:  Until time ?

        Returns:    The time remaining until the next scheduled call or `until_time`, whichever is sooner.

        """
        Scheduler.ourLogger.debug("make_due_calls - time_now: %s, until_time: %s", time_now, until_time)

        sched = Scheduler.ourScheduledCalls
        while sched and sched[0].time <= time_now:
            item = sched.pop(0)
            item.func()
            delay = item.interval
            if delay:
                next_time = item.time + delay
                if next_time < time_now:
                    next_time = time_now + delay
                Scheduler.ourLogger.debug("make_due_calls: rescheduling at: %s", next_time)
                item.time = next_time
                insort(sched, item)
        if sched:
            next_time = min(until_time, sched[0].time)
        else:
            next_time = until_time
        return next_time - time_now
