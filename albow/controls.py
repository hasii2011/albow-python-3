"""
    Albow - Controls
"""

from widget import Widget

from albow.widgets.ButtonBase import ButtonBase
from albow.widgets.Control import Control
from albow.widgets.RadioControl import RadioControl
from albow.widgets.Image import Image
from albow.widgets.CheckWidget import CheckWidget
from albow.widgets.CheckControl import CheckControl

from theme import ThemeProperty


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


class CheckBox(CheckControl, CheckWidget):
    pass


class RadioButton(RadioControl, CheckWidget):
    pass
