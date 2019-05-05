
from pygame.event import Event

from albow.core.Shell import Shell
from albow.core.Widget import Widget


class Screen(Widget):
    """
    Screen is an abstract base class for widgets to be uses as screens by a Shell.
    """
    def __init__(self, shell: Shell, **kwds):
        """
        Constructs a Screen associated with the given shell.
        Args:
            shell: The shell to associate with

            **kwds:
        """
        #
        # Python 3 update
        super().__init__(shell.rect, **kwds)
        self.shell = shell
        self.center = shell.center

    def begin_frame(self):
        """Deprecated, use timer_event() instead."""
        pass
    #
    # Abstract methods follow
    #

    def timer_event(self, event: Event):
        """
        Called from the timer_event() method of the Shell when this screen is the current screen. The default
        implementation returns true so that a display update is performed.

        Args:
            event:

        """
        self.begin_frame()
        return True

    def enter_screen(self):
        """
        Called from the Shell after switching to this screen from another screen.
        """
        pass

    def leave_screen(self):
        """
        Called from the Shell before switching away from this screen to another screen.
        """
        pass
