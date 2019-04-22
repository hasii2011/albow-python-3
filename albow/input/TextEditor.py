
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_TAB
from pygame import draw

from albow.Widget import Widget
from albow.Widget import overridable_property

class TextEditor(Widget):

    upper    = False
    tab_stop = True
    _text    = ""

    def __init__(self, width, upper=None, **kwds):
        """

        :param width:
        :param upper:
        :param kwds:
        """
        super().__init__(**kwds)
        self.set_size_for_text(width)
        if upper is not None:
            self.upper = upper
        self.insertion_point = None

    def get_text(self):
        return self._text

    def set_text(self, text):
        self._text = text

    text = overridable_property('text')

    def draw(self, surface):
        frame = self.get_margin_rect()
        fg = self.fg_color
        font = self.font
        focused = self.has_focus()
        text, i = self.get_text_and_insertion_point()
        if focused and i is None:
            surface.fill(self.sel_color, frame)
        image = font.render(text, True, fg)
        surface.blit(image, frame)
        if focused and i is not None:
            x, h = font.size(text[:i])
            x += frame.left
            y = frame.top
            draw.line(surface, fg, (x, y), (x, y + h - 1))

    def key_down(self, event):
        if not (event.cmd or event.alt):
            k = event.key
            if k == K_LEFT:
                self.move_insertion_point(-1)
                return
            if k == K_RIGHT:
                self.move_insertion_point(1)
                return
            if K_TAB == k:
                self.attention_lost()
                self.tab_to_next()
                return
            try:
                c = event.unicode
            except ValueError:
                c = ""
            #
            # Python 3 update
            #
            # if self.insert_char(c) <> 'pass':
            if self.insert_char(c) != 'pass':
                return
        if event.cmd and event.unicode:
            self.attention_lost()
        self.call_parent_handler('key_down', event)

    def get_text_and_insertion_point(self):
        text = self.get_text()
        i = self.insertion_point
        if i is not None:
            i = max(0, min(i, len(text)))
        return text, i

    def move_insertion_point(self, d):
        text, i = self.get_text_and_insertion_point()
        if i is None:
            if d > 0:
                i = len(text)
            else:
                i = 0
        else:
            i = max(0, min(i + d, len(text)))
        self.insertion_point = i

    def insert_char(self, c):
        if self.upper:
            c = c.upper()
        if c <= "\x7f":
            if c == "\x08" or c == "\x7f":
                text, i = self.get_text_and_insertion_point()
                if i is None:
                    text = ""
                    i = 0
                else:
                    text = text[:i-1] + text[i:]
                    i -= 1
                self.change_text(text)
                self.insertion_point = i
                return
            elif c == "\r" or c == "\x03":
                return self.call_handler('enter_action')
            elif c == "\x1b":
                return self.call_handler('escape_action')
            elif c >= "\x20":
                if self.allow_char(c):
                    text, i = self.get_text_and_insertion_point()
                    if i is None:
                        text = c
                        i = 1
                    else:
                        text = text[:i] + c + text[i:]
                        i += 1
                    self.change_text(text)
                    self.insertion_point = i
                    return
        return 'pass'

    def allow_char(self, c):
        return True

    def mouse_down(self, e):
        self.focus()
        x, y = e.local
        text = self.get_text()
        font = self.font
        # n = len(text)

        def width(idx):
            return font.size(text[:idx])[0]

        i1 = 0
        i2 = len(text)
        x1 = 0
        x2 = width(i2)
        while i2 - i1 > 1:
            i3 = (i1 + i2) // 2
            x3 = width(i3)
            if x > x3:
                i1, x1 = i3, x3
            else:
                i2, x2 = i3, x3
        if x - x1 > (x2 - x1) // 2:
            i = i2
        else:
            i = i1
        self.insertion_point = i

    def change_text(self, text):
        self.set_text(text)
        self.call_handler('change_action')
