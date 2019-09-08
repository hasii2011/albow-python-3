
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
        self.height = self.height / 5
        self.logger: Logger = getLogger(__name__)

    def draw(self, theSurface: Surface):
        """
        We won't honor the margin for the title bar

        Args:
            theSurface: The surface onto which to draw
        """

        w: int = self._rect.width   # syntactic sugar
        h: int = self._rect.height  # syntactic sugar
        borderWidth: int = self.border_width

        self.logger.info(f'w: {w} h: {h} margin: {self.margin} borderWidth: {borderWidth}')

        tBar: Rect = Rect((0, 0), (w, h))
        theSurface.fill(Theme.LAMAS_OFF_WHITE, tBar)
        theSurface.fill(Theme.LAMAS_OFF_WHITE, tBar.inflate(-borderWidth * 2, -borderWidth * 2))

    def draw_over(self, theSurface: Surface):
        """

        Args:
            theSurface:  The surface onto which to draw
        """
        buf = self.font.render(self.title, True, self.fg_color)
        theSurface.blit(buf, (DialogTitleBar.X_OFFSET, DialogTitleBar.Y_OFFSET))
