
from albow.core.ui.Shell import Shell

from albow.demo.screens.GridDebugScreen import GridDebugScreen

DEMO_FRAME_TIME = 50  # ms


class GridDebugShell(Shell):

    """
    Shell
    """
    def __init__(self, display):
        """

        Args:
            display:
        """
        #
        # Python 3 update
        #
        super().__init__(display)

        self.menu_screen = GridDebugScreen(self)  # Do this last
        self.set_timer(DEMO_FRAME_TIME)
        self.show_menu()

    def show_menu(self):
        self.show_screen(self.menu_screen)

    def __repr__(self):
        return self.__class__.__name__
