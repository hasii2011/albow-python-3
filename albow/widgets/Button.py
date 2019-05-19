
import logging

from pygame import Surface
from pygame import Rect
from pygame import draw

from albow.themes.Theme import Theme

from albow.widgets.ButtonBase import ButtonBase
from albow.widgets.Label import Label


class Button(ButtonBase, Label):
    """
    A Button is a widget with a textual label which can be clicked with the mouse to trigger an action.

    """

    def __init__(self, text, action=None, enable=None, **kwds):

        """

        Args:
            text:   Initializes the button with the given text.

            action: The action should be a function with no arguments; it is called
                    when the mouse is clicked and released again inside the button.

            enable: If supplied, enable should be a function
                    that returns a boolean; it will be used to determine whether the button is enabled.
            **kwds:
        """
        self.logger = logging.getLogger(__name__)

        if action:
            kwds['action'] = action
        if enable:
            kwds['enable'] = enable
        Label.__init__(self, text, **kwds)
        self.border_color = Theme.BLACK
        # self.border_width = 1

    def draw_with(self, surface: Surface, fg: tuple, bg: tuple=None):

        self.border_width = 0
        super().draw_with(surface, fg, bg)

        w = self._rect.width   # syntactic sugar
        h = self._rect.height  # syntactic sugar

        # draw border for normal button
        draw.rect(surface, Theme.BLACK, Rect((0, 0, w, h)), 1)       # black border around everything
        draw.line(surface, Theme.WHITE, (1, 1), (w - 2, 1))
        draw.line(surface, Theme.WHITE, (1, 1), (1, h - 2))
        draw.line(surface, Theme.DARK_GRAY, (1, h - 1), (w - 1, h - 1))
        draw.line(surface, Theme.DARK_GRAY, (w - 1, 1), (w - 1, h - 1))
        draw.line(surface, Theme.GRAY, (2, h - 2), (w - 2, h - 2))
        draw.line(surface, Theme.GRAY, (w - 2, 2), (w - 2, h - 2))

    def __repr__(self):
        return self.__class__.__name__
