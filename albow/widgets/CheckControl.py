
from pygame import event

from albow.widgets.Control import Control

class CheckControl(Control):

    def mouse_down(self, e: event):
        self.value = not self.value

    def get_highlighted(self):
        return self.value

