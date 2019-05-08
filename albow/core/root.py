
from time import time
from bisect import insort

from pygame.locals import *
from pygame.time import get_ticks
from pygame.event import Event

from albow.core.ScheduledCall import ScheduledCall

mod_cmd = KMOD_LCTRL | KMOD_RCTRL | KMOD_LMETA | KMOD_RMETA

modifiers = dict(
    shift=False,
    ctrl=False,
    alt=False,
    meta=False,
)

modkeys = {
    K_LSHIFT: 'shift',  K_RSHIFT: 'shift',
    K_LCTRL:  'ctrl',   K_RCTRL:  'ctrl',
    K_LALT:   'alt',    K_RALT:   'alt',
    K_LMETA:  'meta',   K_RMETA:  'meta',
}

scheduled_calls = []


def set_modifier(key, value):
    attr = modkeys.get(key)
    if attr:
        modifiers[attr] = value


def add_modifiers(event):
    d = event.dict
    d.update(modifiers)
    d['cmd'] = event.ctrl or event.meta


def init_timebase():
    global time_base
    time_base = time() * 1000.0 - get_ticks()


def timestamp():
    return time() * 1000.0 - time_base


def make_scheduled_calls():
    #  Legacy
    sched = scheduled_calls
    t = timestamp()
    while sched and sched[0][0] <= t:
        sched[0][1]()
        sched.pop(0)


def make_due_calls(time_now, until_time):
    #  Call all functions scheduled at or before time_now.
    #  Return the time remaining until the next scheduled call
    #  or until_time, whichever is sooner.
    # print "albow.root.make_due_calls:", time_now, until_time ###
    sched = scheduled_calls
    while sched and sched[0].time <= time_now:
        item = sched.pop(0)
        item.func()
        delay = item.interval
        if delay:
            next_time = item.time + delay
            if next_time < time_now:
                next_time = time_now + delay
            # print "albow.root.make_due_calls: rescheduling at", next_time ###
            item.time = next_time
            insort(sched, item)
    if sched:
        next_time = min(until_time, sched[0].time)
    else:
        next_time = until_time
    return next_time - time_now


def schedule_event(delay, func, repeat=False):

    def thunk():
        #
        # Pygame 1.9 update
        #
        # event = Event(USEREVENT, time = timestamp())
        event = Event(USEREVENT, dict=None)
        add_modifiers(event)
        func(event)

    Scheduler.schedule_call(delay, thunk, repeat)


def cancel_call(token):
    """
    Cancel a previously scheduled call, given a token returned by
    schedule_call or schedule_event.
    """
    try:
        scheduled_calls.remove(token)
    except ValueError:
        pass


class Scheduler:
    """
    A static class to avoid using module functions
    """
    @staticmethod
    def schedule(delay, func):
        """
        Deprecated, use schedule_call or schedule_event instead.
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
        """
        t = timestamp() + delay
        if repeat:
            r = delay
        else:
            r = 0.0
        item = ScheduledCall(t, func, r)
        insort(scheduled_calls, item)
        return item
