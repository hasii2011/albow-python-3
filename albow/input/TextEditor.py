
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame.locals import K_TAB
from pygame import draw

from albow.utils import overridable_property

from albow.core.Widget import Widget


class TextEditor(Widget):
    """
    A TextEditor provides simple single-line text editing.  Typed characters are inserted into the text, and
    characters are deleted using `Delete` or `Backspace`.  Clicking on the text field gives it the keyboard focus
    and sets the insertion point.  Pressing the Tab key moves to the next widget that has a tab stop.

    .. Note::
        There is currently no support for selecting or copying and pasting text.
    """

    text = overridable_property('text')
    """
    The current text, provided the get_text and set_text methods have not been overridden.
    """
    upper = False
    """
    If true, text typed into the field is forced to upper case.
    """
    tab_stop = True
    """
    If True this widget is a tab stop
    """
    insertionPoint = None
    """
    The current position of the insertion point. May be set to None to position it at the end of the text.
    """
    enterAction = None
    """
    .. TODO::
        A function of no arguments to be called when Return or Enter is pressed. If not specified, `Return` and `Enter` 
        key events are passed to the parent widget.
    """
    escapeAction = None
    """
    .. TODO::
        A function of no arguments to be called when `Escape` is pressed. If not specified, Escape key events are 
        passed to the parent widget.
    """
    _text    = ""

    def __init__(self, width, upper: bool=None, **kwds):
        """
        The height is determined by the height of a line of text in the font in effect at construction time.

        Args:
            width:  The width can be either an integer or a string.  If an integer, it specifies the width in
                    pixels; if a string, the widget is made just wide enough to contain the given text.

            upper:  If `True` then upper-case the next; If `False` or `None` then we keep out mitts of the text ;-)

            **kwds:
        """
        super().__init__(**kwds)
        self.set_size_for_text(width)
        if upper is not None:
            self.upper = upper
        self.insertionPoint = None

    def get_text(self):
        return self._text

    def set_text(self, theNewText):
        """
        Internally, the widget uses these methods to access the text being edited. By default they access text held 
        in a private attribute. By overriding them, you can arrange for the widget to edit text being held 
        somewhere else.
        
        Args:
            theNewText: 

        """
        self._text = theNewText

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

    def key_down(self, theKeyEvent):
        if not (theKeyEvent.cmd or theKeyEvent.alt):
            k = theKeyEvent.key
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
                c = theKeyEvent.unicode
            except ValueError:
                c = ""
            #
            # Python 3 update
            #
            # if self.insert_char(c) <> 'pass':
            if self.insert_char(c) != 'pass':
                return
        if theKeyEvent.cmd and theKeyEvent.unicode:
            self.attention_lost()
        self.call_parent_handler('key_down', theKeyEvent)

    def get_text_and_insertion_point(self):
        text = self.get_text()
        i = self.insertionPoint
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
        self.insertionPoint = i

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
                self.insertionPoint = i
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
                    self.insertionPoint = i
                    return
        return 'pass'

    def allow_char(self, c):
        """
        This method meant to be overriden

        Called to determine whether typing the character c into the text editor should be allowed. The default
        implementation returns true for all characters.

        Args:
            c: The character to determine if allowed

        Returns: If allowed True, else false

        """
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
        self.insertionPoint = i

    def change_text(self, text):
        self.set_text(text)
        self.call_handler('change_action')
