
from pygame import Rect
from pygame import Surface
from pygame import draw

from albow.core.Widget import Widget

from albow.themes.ThemeProperty import ThemeProperty

class CheckWidget(Widget):

    default_size     = (16, 16)
    margin           = 4
    border_width     = 1
    check_mark_tweak = 2

    smooth = ThemeProperty('smooth')

    def __init__(self, **kwds):
        super().__init__(Rect((0, 0), self.default_size), **kwds)

    def draw(self, theSurface: Surface):
        '''

        :param theSurface:  The surface to draw on
        '''
        if self.highlighted:
            r = self.get_margin_rect()
            fg = self.fg_color
            d = self.check_mark_tweak
            p1 = (r.left, r.centery - d)
            p2 = (r.centerx - d, r.bottom)
            p3 = (r.right, r.top - d)
            if self.smooth:
                draw.aalines(theSurface, fg, False, [p1, p2, p3])
            else:
                draw.lines(theSurface, fg, False, [p1, p2, p3])

