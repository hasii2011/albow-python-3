
from albow.widgets.ButtonBase import ButtonBase
from albow.widgets.Label import Label

class Button(ButtonBase, Label):
    """
    Eeks multiple inheritance
    """

    def __init__(self, text, action=None, enable=None, **kwds):
        if action:
            kwds['action'] = action
        if enable:
            kwds['enable'] = enable
        Label.__init__(self, text, **kwds)

