
from pygame import event
from albow.widgets.Control import Control

class RadioControl(Control):

    setting = None
    """
    The setting of the value that this radio button corresponds to.
    """

    def get_highlighted(self):
        return self.value == self.setting

    def mouse_down(self, e: event):
        self.value = self.setting

