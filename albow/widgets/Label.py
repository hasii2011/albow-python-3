
import logging

from Widget import overridable_property
from Widget import Widget
from theme import ThemeProperty

class Label(Widget):
    """

    """

    text  = overridable_property('text')
    align = overridable_property('align')

    highlight_color    = ThemeProperty('highlight_color')
    disabled_color     = ThemeProperty('disabled_color')
    highlight_bg_color = ThemeProperty('highlight_bg_color')
    enabled_bg_color   = ThemeProperty('enabled_bg_color')
    disabled_bg_color  = ThemeProperty('disabled_bg_color')

    enabled     = True
    highlighted = False
    _align = 'l'

    def __init__(self, text, width=None, **kwds):
        """

        :param text:
        :param width:
        :param kwds:
        """

        # print( "__class__: '" + self.__class__.__name__ + "'")
        #
        # Use this naming convention, until I break these out into separate packages
        #
        self.logger = logging.getLogger(self.__class__.__name__)

        super().__init__(**kwds)
        font = self.font
        lines = text.split("\n")
        tw, th = 0, 0
        for line in lines:
            w, h = font.size(line)
            tw = max(tw, w)
            th += h
        if width is not None:
            tw = width
        else:
            tw = max(1, tw)
        d = 2 * self.margin
        adjustedWidth   = tw + d
        adjustedHeight  = th + d
        # self.size = (tw + d, th + d)
        self.size = (adjustedWidth, adjustedHeight)   # Python 3 update
        self._text = text
        self.logger.debug("Control size %s", self.size)

    def get_text(self):
        return self._text

    def set_text(self, x):
        self._text = x

    def get_align(self):
        return self._align

    def set_align(self, x):
        self._align = x

    def draw(self, surface):
        """

        :param surface:
        :return:
        """
        if not self.enabled:
            fg = self.disabled_color
            bg = self.disabled_bg_color
        elif self.highlighted:
            fg = self.highlight_color
            bg = self.highlight_bg_color
        else:
            fg = self.fg_color
            bg = self.enabled_bg_color
        self.draw_with(surface, fg, bg)

    def draw_with(self, surface, fg, bg=None):
        """

        :param surface:
        :param fg:
        :param bg:
        :return:
        """
        if bg:
            r = surface.get_rect()
            b = self.border_width
            if b:
                e = - 2 * b
                r.inflate_ip(e, e)
            surface.fill(bg, r)
        m = self.margin
        align = self.align
        width = surface.get_width()
        y = m
        lines = self.text.split("\n")
        font = self.font
        dy = font.get_linesize()
        for line in lines:
            image = font.render(line, True, fg)
            r = image.get_rect()
            r.top = y
            if align == 'l':
                r.left = m
            elif align == 'r':
                r.right = width - m
            else:
                r.centerx = width // 2
            surface.blit(image, r)
            y += dy

