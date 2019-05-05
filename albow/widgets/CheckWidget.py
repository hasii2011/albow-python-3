
from pygame import Rect
from pygame import Surface
from pygame import draw

from albow.core.Widget import Widget

from albow.themes.ThemeProperty import ThemeProperty

CHECK_MARK_TWEAK = 2


class CheckWidget(Widget):

    default_size     = (16, 16)
    """
    The default size of the checkbox;  Default is 16x16
    """
    margin           = 4
    """
    The margin around the check mark;  Default is 4
    """
    border_width     = 1
    """
        This border width of the rectangle around the checkmark;  Default is 1
    """

    smooth = ThemeProperty('smooth')
    """
        Set to True if you want the checkmark anti-aliased;  Default is True
    """

    def __init__(self, **kwds):
        super().__init__(Rect((0, 0), self.default_size), **kwds)

    def draw(self, theSurface: Surface):
        """

        Args:
            theSurface:  The surface to draw on


        """
        if self.highlighted:
            r = self.get_margin_rect()
            fg = self.fg_color
            d = CHECK_MARK_TWEAK
            p1 = (r.left, r.centery - d)
            p2 = (r.centerx - d, r.bottom)
            p3 = (r.right, r.top - d)
            if self.smooth:
                draw.aalines(theSurface, fg, False, [p1, p2, p3])
            else:
                draw.lines(theSurface, fg, False, [p1, p2, p3])

