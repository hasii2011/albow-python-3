
from pygame import event
from albow.widgets.Control import Control

class RadioControl(Control):

    setting = None

    def get_highlighted(self):
        return self.value == self.setting

    def mouse_down(self, e: event):
        self.value = self.setting

