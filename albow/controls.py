"""
    Albow - Controls
"""

from pygame import Rect, draw
from widget import Widget

from albow.widgets.Control import Control
from albow.widgets.Label import Label
from albow.widgets.Image import Image
from albow.widgets.CheckWidget import CheckWidget

from theme import ThemeProperty
from utils import blit_in_rect


class AttrRef(object):
    """
    AttrRef is here for backwards compatibility.
    New code should use references.Ref instead.
    """

    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr

    def get(self):
        return getattr(self.obj, self.attr)

    def set(self, x):
        setattr(self.obj, self.attr, x)


class ItemRef(object):
    """
    ItemRef is here for backwards compatibility.
    New code should use references.Ref instead.
    """

    def __init__(self, obj, item):
        self.obj  = obj
        self.item = item

    def get(self):
        # return self.obj[item]
        return self.obj[self.item]   # Python 3 update

    def set(self, x):
        # self.obj[item] = x
        self.obj[self.item] = x     # Python 3 update


class ButtonBase(Control):

    align = 'c'
    action = None

    def mouse_down(self, event):
        if self.enabled:
            self._highlighted = True

    def mouse_drag(self, event):
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

    def set_enabled(self, x):
        self._enabled = x


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


class ImageButton(ButtonBase, Image):

    disabled_bg_image = ThemeProperty('disabled_bg_image')
    enabled_bg_image = ThemeProperty('enabled_bg_image')
    highlighted_bg_image = ThemeProperty('highlighted_bg_image')

    def draw(self, surf):
        dbi = self.disabled_bg_image
        ebi = self.enabled_bg_image
        hbi = self.highlighted_bg_image
        # fgi = self.image              Python 3 update, variable unused
        if not self.enabled:
            if dbi:
                self.draw_image(surf, dbi)
        elif self.highlighted:
            if hbi:
                self.draw_image(surf, hbi)
            else:
                surf.fill(self.highlight_color)
        else:
            if ebi:
                self.draw_image(surf, ebi)
        fgi = self.image
        if fgi:
            self.draw_image(surf, fgi)


class ValueDisplay(Control, Widget):

    format = "%s"
    align = 'l'

    def __init__(self, width=100, **kwds):

        Widget.__init__(self, **kwds)
        self.set_size_for_text(width)

    def draw(self, surf):
        value = self.value
        text = self.format_value(value)
        buf = self.font.render(text, True, self.fg_color)
        frame = surf.get_rect()
        blit_in_rect(surf, buf, frame, self.align, self.margin)

    def format_value(self, value):
        if value is not None:
            return self.format % value
        else:
            return ""


class CheckControl(Control):

    def mouse_down(self, e):
        self.value = not self.value

    def get_highlighted(self):
        return self.value


class CheckBox(CheckControl, CheckWidget):
    pass


class RadioControl(Control):

    setting = None

    def get_highlighted(self):
        return self.value == self.setting

    def mouse_down(self, e):
        self.value = self.setting


class RadioButton(RadioControl, CheckWidget):
    pass
