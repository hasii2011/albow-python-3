
import logging

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
