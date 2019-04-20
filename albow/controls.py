"""
    Albow - Controls
"""

from pygame import Rect, draw
from widget import Widget, overridable_property
from albow.widgets.Control import Control

from albow.widgets.Label import Label
from theme import ThemeProperty
from utils import blit_in_rect
import resource


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


# class Label(Widget):
#     """
#
#     """
#
#     text  = overridable_property('text')
#     align = overridable_property('align')
#
#     highlight_color    = ThemeProperty('highlight_color')
#     disabled_color     = ThemeProperty('disabled_color')
#     highlight_bg_color = ThemeProperty('highlight_bg_color')
#     enabled_bg_color   = ThemeProperty('enabled_bg_color')
#     disabled_bg_color  = ThemeProperty('disabled_bg_color')
#
#     enabled     = True
#     highlighted = False
#     _align = 'l'
#
#     def __init__(self, text, width=None, **kwds):
#         """
#
#         :param text:
#         :param width:
#         :param kwds:
#         """
#
#         # print( "__class__: '" + self.__class__.__name__ + "'")
#         #
#         # Use this naming convention, until I break these out into separate packages
#         #
#         self.logger = logging.getLogger(self.__class__.__name__)
#
#         Widget.__init__(self, **kwds)
#         font = self.font
#         lines = text.split("\n")
#         tw, th = 0, 0
#         for line in lines:
#             w, h = font.size(line)
#             tw = max(tw, w)
#             th += h
#         if width is not None:
#             tw = width
#         else:
#             tw = max(1, tw)
#         d = 2 * self.margin
#         adjustedWidth   = tw + d
#         adjustedHeight  = th + d
#         # self.size = (tw + d, th + d)
#         self.size = (adjustedWidth, adjustedHeight)   # Python 3 update
#         self._text = text
#         self.logger.debug("Control size %s", self.size)
#
#     def get_text(self):
#         return self._text
#
#     def set_text(self, x):
#         self._text = x
#
#     def get_align(self):
#         return self._align
#
#     def set_align(self, x):
#         self._align = x
#
#     def draw(self, surface):
#         """
#
#         :param surface:
#         :return:
#         """
#         if not self.enabled:
#             fg = self.disabled_color
#             bg = self.disabled_bg_color
#         elif self.highlighted:
#             fg = self.highlight_color
#             bg = self.highlight_bg_color
#         else:
#             fg = self.fg_color
#             bg = self.enabled_bg_color
#         self.draw_with(surface, fg, bg)
#
#     def draw_with(self, surface, fg, bg=None):
#         """
#
#         :param surface:
#         :param fg:
#         :param bg:
#         :return:
#         """
#         if bg:
#             r = surface.get_rect()
#             b = self.border_width
#             if b:
#                 e = - 2 * b
#                 r.inflate_ip(e, e)
#             surface.fill(bg, r)
#         m = self.margin
#         align = self.align
#         width = surface.get_width()
#         y = m
#         lines = self.text.split("\n")
#         font = self.font
#         dy = font.get_linesize()
#         for line in lines:
#             image = font.render(line, True, fg)
#             r = image.get_rect()
#             r.top = y
#             if align == 'l':
#                 r.left = m
#             elif align == 'r':
#                 r.right = width - m
#             else:
#                 r.centerx = width // 2
#             surface.blit(image, r)
#             y += dy
#

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


class Image(Widget):
    #  image   Image to display

    highlight_color = ThemeProperty('highlight_color')
    image           = overridable_property('image')
    highlighted     = False

    def __init__(self, image=None, rect=None, **kwds):
        Widget.__init__(self, rect, **kwds)
        if image:
            # if isinstance(image, basestring):
            if isinstance(image, str):			# Python 3 update probably not necessary -- hasii
                image = resource.get_image(image)
            w, h = image.get_size()
            d = 2 * self.margin
            self.size = w + d, h + d
            self._image = image

    def get_image(self):
        return self._image

    def set_image(self, x):
        self._image = x

    def draw(self, surf):
        if self.highlighted:
            surf.fill(self.highlight_color)
        self.draw_image(surf, self.image)

    def draw_image(self, surf, image):
        frame = surf.get_rect()
        r = image.get_rect()
        r.center = frame.center
        surf.blit(image, r)


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


class CheckWidget(Widget):

    default_size = (16, 16)
    margin = 4
    border_width = 1
    check_mark_tweak = 2

    smooth = ThemeProperty('smooth')

    def __init__(self, **kwds):
        Widget.__init__(self, Rect((0, 0), self.default_size), **kwds)

    def draw(self, surf):
        if self.highlighted:
            r = self.get_margin_rect()
            fg = self.fg_color
            d = self.check_mark_tweak
            p1 = (r.left, r.centery - d)
            p2 = (r.centerx - d, r.bottom)
            p3 = (r.right, r.top - d)
            if self.smooth:
                draw.aalines(surf, fg, False, [p1, p2, p3])
            else:
                draw.lines(surf, fg, False, [p1, p2, p3])


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
