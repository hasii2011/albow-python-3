
from pygame.event import Event

from pygame import Surface

from albow.core.RootWidget import RootWidget


class Shell(RootWidget):
    """
    The Shell class is an abstract class to use as a base for the outer shell of a game. It provides facilities
    for switching between a number of screens, such as menus, pages of instructions or the game itself. Screens
    are normally subclasses of the Screen widget.
    """

    def __init__(self, surface: Surface, **kwds):
        """
        Initializes the Shell with the given surface as its root surface (normally this will be the PyGame
        screen surface).

        Args:
            surface:  A pygame surface
            **kwds:
        """
        #
        # Python 3 update
        #
        super().__init__(surface, **kwds)
        self.current_screen = None

    def show_screen(self, new_screen):
        """
        Hides the previous screen, if any, and shows the given widget as the new screen. The widget is displayed
        centered within the shell.

        The leave_screen() method of the previous screen is called before hiding it, and the enter_screen() method
        of the new screen is called after showing it.

        TODO fix screen imports shell & shell imports screen

        Args:
            new_screen:  The new screen to display

        Returns:

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
        """
        Calls the timer_event() method of the current screen, if any, and returns its result.
        Args:
            event: An event

        Returns:  The result

        """
        screen = self.current_screen
        if screen:
            return screen.timer_event(event)

    def begin_frame(self):
        """
        Deprecated, use timer_event() instead.
        """
        screen = self.current_screen
        if screen:
            screen.begin_frame()

    def relative_mode(self):
        """
        A Shell runs in relative input mode if the current screen does.
        """
        screen = self.current_screen
        return screen and screen.relative_mode()
