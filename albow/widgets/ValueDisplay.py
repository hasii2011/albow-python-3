
from pygame import Surface

from albow.core.Widget import Widget

from albow.widgets.Control import Control

from albow.utils import blit_in_rect

class ValueDisplay(Control, Widget):

    """
    A ValueDisplay is a Control that provides a read-only textual display of a value.
    """
    format = "%s"
    """
    Format string to be used when displaying the value. Also see the format_value() method below.

    """
    align  = 'l'
    """
        How to align the value.  Default is 'l'
    """

    def __init__(self, width=100, **kwds):

        Widget.__init__(self, **kwds)
        self.set_size_for_text(width)

    def draw(self, surface: Surface):

        value = self.value
        text  = self.format_value(value)
        buf   = self.font.render(text, True, self.fg_color)
        frame = surface.get_rect()
        blit_in_rect(surface, buf, frame, self.align, self.margin)

    def format_value(self, value):
        if value is not None:
            return self.format % value
        else:
            return ""
