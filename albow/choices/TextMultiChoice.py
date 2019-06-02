
from pygame import draw
from pygame import Surface
from pygame import Rect

from albow.utils import blit_in_rect


from albow.choices.MultiChoice import MultiChoice


class TextMultiChoice(MultiChoice):
    """
    TextMultichoice is a Multichoice control that displays its values in the form of text.

    .. Note::
        In addition to the highlight styles defined by PaletteView,
        TextMultichoice also provides 'arrows', which highlights the selected value with a pair of
        arrowheads above and below.

    """
    def __init__(self, values, labels=None, **kwds):
        """

        Initializes the control with the given values and corresponding labels. If no labels are specified,
        they are derived by applying str() to the values

        Args:
            values: The values

            labels: The displayed associated labels

            **kwds:
        """

        if not labels:
            labels = map(str, values)
        font = self.predict_font(kwds)
        # d = 2 * self.predict(kwds, 'margin')
        cd = 2 * self.predict(kwds, 'cell_margin')
        wmax = 0
        hmax = 0

        for (w, h) in map(font.size, labels):
            wmax = max(wmax, w)
            hmax = max(hmax, h)
        cw = wmax + cd
        ch = hmax + cd

        super().__init__((cw, ch), values, **kwds)

        self.labels = labels

    def draw_item(self, theSurface: Surface, n: int, theRect: Rect):

        buf = self.font.render(self.labels[n], True, self.fg_color)
        blit_in_rect(theSurface, buf, theRect, self.align, self.margin)

    def draw_prehighlight(self, theSurface: Surface, theItemNumber: int, theRect: Rect):
        if self.highlight_style == 'arrows':
            self.draw_arrows(theSurface, theRect)
        else:
            MultiChoice.draw_prehighlight(self, theSurface, theItemNumber, theRect)

    def draw_arrows(self, theSurface: Surface, theRect: Rect):
        """

        Args:
            theSurface: pygame surface to drawn

            theRect: The pygame rectangle to draw in

        """
        m = self.margin
        color = self.sel_color or self.fg_color
        x, y = theRect.midtop
        pts = [(x - m, y - m), (x + m, y - m), (x, y)]
        draw.polygon(theSurface, color, pts)
        x, y = theRect.midbottom
        y -= 1
        pts = [(x - m, y + m), (x + m, y + m), (x, y)]
        draw.polygon(theSurface, color, pts)
