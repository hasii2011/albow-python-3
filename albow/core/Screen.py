
from pygame.event import Event

from albow.core.shell import Shell
from albow.core.Widget import Widget

class Screen(Widget):

    def __init__(self, shell: Shell, **kwds):
        """

        :param shell:
        :param kwds:
        """
        #
        # Python 3 update
        super().__init__(shell.rect, **kwds)
        self.shell = shell
        self.center = shell.center

    def timer_event(self, event: Event):
        self.begin_frame()
        return True

    def begin_frame(self):
        """Deprecated, use timer_event() instead."""
        pass

    def enter_screen(self):
        pass

    def leave_screen(self):
        pass

