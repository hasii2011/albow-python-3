#
#   Albow - Screen
#

from widget_file import Widget

#------------------------------------------------------------------------------

class Screen(Widget):

    def __init__(self, shell, **kwds):
        """

        :param shell:
        :param kwds:
        """
        #
        # Python 3 update
        super().__init__(shell.rect, **kwds)
        self.shell = shell
        self.center = shell.center

    def timer_event(self, event):
        self.begin_frame()
        return True

    def begin_frame(self):
        """Deprecated, use timer_event() instead."""
        pass

    def enter_screen(self):
        pass

    def leave_screen(self):
        pass

