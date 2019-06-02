
from pygame import Surface

from albow.core.Shell import Shell

from org.hasii.pytrek.albow.StarTrekScreen import StarTrekScreen


class StarTrekShell(Shell):

    FRAME_TIME = 30
    """
    In milliseconds
    """

    def __init__(self, theSurface: Surface, **kwds):

        super().__init__(theSurface, **kwds)

        self.set_timer(StarTrekShell.FRAME_TIME)

        self.screen: StarTrekScreen = StarTrekScreen(shell=self, theSurface=theSurface)
        self.show_screen(self.screen)