
import logging

from pygame import Surface

from albow.utils import overridable_property

from albow.core.Widget import Widget
from albow.themes.ThemeProperty import ThemeProperty


class Label(Widget):
    """
    Initializes the label with the given text and font. If a width is specified, it is used, otherwise the
    label is initially made just wide enough to contain the text. The text may consist of more than one line,
    separated by '\\n'. The initial height is determined by the number of lines and the font specified at
    construction time or the default font from the theme.
    """

    """
    Properties
    """
    text  = overridable_property('text')
    """
    The text to be displayed. This can be changed dynamically, but the label won't automatically resize to 
    accommodate the new text.
    """
    align = overridable_property('align')
    """
    Specifies the alignment of the text within the widget's rect. One of 'l', 'c' or 'r' for left, center or 
    right.
    """

    highlight_color    = ThemeProperty('highlight_color')
    """The color to use for highlighting the label"""
    disabled_color     = ThemeProperty('disabled_color')
    """The color to use when the label is disabled"""
    highlight_bg_color = ThemeProperty('highlight_bg_color')
    """The highlight background color"""
    enabled_bg_color   = ThemeProperty('enabled_bg_color')
    """The enabled background color"""
    disabled_bg_color  = ThemeProperty('disabled_bg_color')
    """The disabled background color"""

    enabled     = True
    """Indicates if label should be enabled.  Defaults to True"""
    highlighted = False
    """
    Indicates whether the label should be highlighted.  Defaults to False.  If set to true you MUST define
    highlight_color
    """
    _align = 'l'

    def __init__(self, text, width=None, **kwds):
        """

        Args:
            text:   The label text
            width:  The width of the label
            **kwds: Additional key value pairs that affect the label
        """
        self.logger = logging.getLogger(__name__)

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

    def draw(self, surface: Surface):
        # """
        #
        # :param surface:  The surface onto which to draw
        # :return:
        # """
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

    def draw_with(self, surface: Surface, fg: tuple, bg: tuple=None):
        """

        Args:
            surface:  The surface to drawn on
            fg:       The foreground color
            bg:       The background color

        Returns:

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

