"""
        .. WARNING::
            This is warning text

        .. ATTENTION::
            This is attention text

        .. CAUTION::
            This is caution text

        .. DANGER::
            This is danger text

        .. ERROR::
            This is error text

        .. HINT::
            This is hint text

        .. IMPORTANT::
            This is important text

        .. NOTE::
            This is note text

        .. TIP::
            This is tip text

"""
from time import time

from pygame.locals import *

from pygame.time import get_ticks

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

time_base = 0


class CoreUtilities:
    """
    A static class for some leftover module functions
    """
    @staticmethod
    def set_modifier(key, value):
        attr = modkeys.get(key)
        if attr:
            modifiers[attr] = value

    @staticmethod
    def add_modifiers(event):
        d = event.dict
        d.update(modifiers)
        d['cmd'] = event.ctrl or event.meta

    @staticmethod
    def init_timebase():
        global time_base
        time_base = time() * 1000.0 - get_ticks()
        print("time_base: " + str(time_base))
