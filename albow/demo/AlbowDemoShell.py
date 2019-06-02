
from pygame import Surface

from albow.core.ui.Shell import Shell

from albow.demo.AlbowDemoScreen import AlbowDemoScreen


class AlbowDemoShell(Shell):

    FRAME_TIME = 30
    """
    In milliseconds
    """

    def __init__(self, theSurface: Surface, **kwds):

        super().__init__(theSurface, **kwds)

        self.set_timer(AlbowDemoShell.FRAME_TIME)

        self.screen: AlbowDemoScreen = AlbowDemoScreen(shell=self, theSurface=theSurface)
        self.show_screen(self.screen)