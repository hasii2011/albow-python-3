
from pygame.event import Event

from pygame import Surface

from albow.core.RootWidget import RootWidget


class Shell(RootWidget):
    """

    """

    def __init__(self, surface: Surface, **kwds):
        #
        # Python 3 update
        #
        super().__init__(surface, **kwds)
        self.current_screen = None

    def show_screen(self, new_screen):
        """

        :param new_screen:   TODO fix screen imports shell & shell imports screen
        :return:
        """

        old_screen = self.current_screen
        if old_screen is not new_screen:
            if old_screen:
                old_screen.leave_screen()
            self.remove(old_screen)
            self.add(new_screen)
            self.current_screen = new_screen
            if new_screen:
                new_screen.focus()
                new_screen.enter_screen()
                self.invalidate()

    def timer_event(self, event: Event):
        screen = self.current_screen
        if screen:
            return screen.timer_event(event)

    def begin_frame(self):
        """Deprecated, use timer_event() instead."""
        screen = self.current_screen
        if screen:
            screen.begin_frame()

    def relative_mode(self):
        """A Shell runs in relative input mode if the current screen does."""
        screen = self.current_screen
        return screen and screen.relative_mode()
