
from pygame import event

from albow.widgets.Control import Control


class ButtonBase(Control):

    align = 'c'
    action = None

    def mouse_down(self, event):
        if self.enabled:
            self._highlighted = True

    def mouse_drag(self, theEvent: event):
        state = event in self
        # if state <> self._highlighted:
        if state != self._highlighted:
            self._highlighted = state
            self.invalidate()

    def mouse_up(self, event):
        if event in self:
            self._highlighted = False
            if self.enabled:
                self.call_handler('action')

    def get_highlighted(self):
        return self._highlighted

    def get_enabled(self):
        enable = self.enable
        if enable:
            return enable()
        else:
            return self._enabled

    def set_enabled(self, theNewValue: bool):
        self._enabled = theNewValue
