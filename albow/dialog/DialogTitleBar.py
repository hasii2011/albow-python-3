
from pygame import Surface
from pygame import Rect

from logging import Logger
from logging import getLogger

from albow.core.ui.Widget import Widget

from albow.themes.Theme import Theme


class DialogTitleBar(Widget):

    Y_OFFSET: int = 2
    X_OFFSET: int = 5

    def __init__(self, theTitle: str = 'Default Title', **kwds):

        self.title: str = theTitle

        super().__init__(**kwds)

        self.height: int    = self.height // 5
        self.border_width   = 1
        self.logger: Logger = getLogger(__name__)

    def draw(self, theSurface: Surface):
        """
        Args:
            theSurface: The surface onto which to draw
        """
        w: int = self._rect.width   # syntactic sugar
        h: int = self._rect.height  # syntactic sugar

        self.logger.debug(f'w: {w} h: {h} margin: {self.margin}')

        tBar: Rect = Rect((0, 0), (w, h))
        self.logger.debug(f'tBar: {tBar}  theSurface: {theSurface}')
        theSurface.fill(Theme.LAMAS_OFF_WHITE, tBar)

    def draw_over(self, theSurface: Surface):
        """

        Args:
            theSurface:  The surface onto which to draw
        """
        buf = self.font.render(self.title, True, self.fg_color)
        theSurface.blit(buf, (DialogTitleBar.X_OFFSET, DialogTitleBar.Y_OFFSET))
