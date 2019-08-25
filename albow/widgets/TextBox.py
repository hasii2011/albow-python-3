
from typing import List

import logging

from pygame import Surface
from pygame import Rect
from pygame import draw
from pygame.event import Event

from albow.core.ui.Widget import Widget

from albow.themes.ThemeProperty import ThemeProperty


class TextBox(Widget):
    """
    This is a basic _read-only_ multi-line display widget with support for scrolling.  Currently,
    the API consumer breaks up lines via the `LINE_SEPARATOR` character.  The widget automatically
    displays scroll buttons when the number of lines in `text` exceeds the `numberOfRows`

    """
    LINE_SEPARATOR = "\n"
    """
    The character to use to break up lines in the text widget
    """
    CANONICAL_WIDEST_TALLEST_CHARACTER = "W"
    NO_TEXT = ''

    disabled_color = ThemeProperty('disabled_color')
    """
    The color to use when the text box is disabled
    """
    enabled_bg_color = ThemeProperty('enabled_bg_color')
    """
    The enabled background color
    """
    disabled_bg_color = ThemeProperty('disabled_bg_color')
    """
    The disabled background color
    """
    scroll_button_size = ThemeProperty('scroll_button_size')
    """
    Size of the scrolling buttons. This is a number, not a tuple -- the scroll buttons are square.
    """
    scroll_button_color = ThemeProperty('scroll_button_color')
    """
        Color in which to draw the scrolling buttons.
    """
    def __init__(self, theText: str = "", theNumberOfColumns: int = 28, theNumberOfRows: int = 6, **kwds):
        """

        Args:
            theText:   The text to display in the multi-line widget

            theNumberOfColumns:  The number of columns to display.  One column is one character

            theNumberOfRows:  The number of rows to display.  One text line is one row

            **kwds: Additional key value pairs that affect the text widget
        """

        self.logger = logging.getLogger(__name__)

        super().__init__(**kwds)

        self.margin = 4
        lines: List = []
        if theText is not None:
            lines = theText.strip().split(TextBox.LINE_SEPARATOR)
        self.lines = lines
        """ Saves the broken up lines"""
        self.numberOfColumns = theNumberOfColumns
        """The number of columns in the widget"""
        self.numberOfRows    = theNumberOfRows
        """The number of rows in the widget"""
        self.firstIdx = 0
        """"The index into `lines` as the first line to display"""
        self.lastIdx  = 0
        """The index into `lines` as the last line to display"""
        self.size = self.computeBoxSize(theNumberOfColumns, theNumberOfRows)
        self.logger.debug(f"size: {self.size}")

        self.lastInsertedVisible = True
        """If `True` whenever the developer inserts a new line then the widget scrolls, if necessary to keep it visible"""
        self.firstRow = 0
        """What scroll bars think the first row index is"""
        self._text = theText
        self._lastInsertedVisible = True

        self.debugJustInserted = False

    def getText(self):
        return self._text

    def setText(self, theNewText: str):
        """
        Replace the contents with this new text

        Args:
            theNewText:  The text that replaces what was in the widget

        """
        lines = theNewText.strip().split(TextBox.LINE_SEPARATOR)
        self.lines = lines
        self.debugJustInserted = True

        self.logger.debug(f"# of lines: {len(self.lines)}")
        self._text = theNewText
        self._recomputeTextToDisplayIndices()

    text = property(getText, setText)
    """
    The text to be displayed. This can be changed dynamically
    """

    def getLastInsertedVisible(self):
        return self._lastInsertedVisible

    def setLastInsertedVisible(self, theNewValue: bool):
        self._lastInsertedVisible = theNewValue

    lastInsertedVisible = property(getLastInsertedVisible, setLastInsertedVisible)

    def addText(self, newText: str):
        """
        Different than setText.  This appends the new text to the contents of the widget

        Args:
            newText:  The new text to append to the text widget

        """
        oldLines: str = self.getText()

        oldLines += f"{newText}{TextBox.LINE_SEPARATOR}"
        self.setText(oldLines)

    def insertText(self, theNewLine):
        """

        Args:
            theNewLine:
        """
        oldLines: str = self.getText()
        oldLines = f"{theNewLine}{TextBox.LINE_SEPARATOR}" + oldLines
        self.setText(oldLines)

    def deleteText(self, theLineNumber: int = 0):
        """
        Lines are defined as strings of text separated by `TextBox.LINE_SEPARATOR`
        Can't delete any lines if widget is empty (operation is ignored)
        Can't delete a line that does not exist (operation is ignored)

        Args:
            theLineNumber:  The line number to delete;  Defaults to the first line (numbered 0)
        """
        if len(self.getText()) > 0:
            oldLines: str       = self.getText()
            splits:   List[str] = oldLines.splitlines(True)
            self.logger.info(f'splits: {splits}')

            if len(splits) > theLineNumber:
                del splits[theLineNumber]
                newLines: str = ''.join(splits)
                self.logger.info(f'newLines: {newLines}')

                self.setText(newLines)

    def clearText(self):
        """
        Empties the text widget
        """
        self.firstIdx = 0
        self.lastIdx  = 0
        self.setText(TextBox.NO_TEXT)

    def draw(self, theSurface: Surface):
        """

        Args:
            theSurface:  The surface onto which to draw

        """
        r = theSurface.get_rect()
        b = self.border_width
        if b:
            e = - 2 * b
            r.inflate_ip(e, e)
        theSurface.fill(self.bg_color, r)

        x = self.margin
        y = self.margin

        if self.logger.level == logging.DEBUG:
            if self.debugJustInserted is True:
                self.debugJustInserted = False
                self.logger.debug(f"firstIdx: {self.firstIdx} lastIdx: {self.lastIdx}")

        for idx in range(self.firstIdx, self.lastIdx):

            buf = self.font.render(self.lines[idx], True, self.fg_color)
            theSurface.blit(buf, (x, y))
            y += buf.get_rect().height

        if len(self.lines) > self.numberOfRows:
            self.draw_scroll_up_button(theSurface)
            self.draw_scroll_down_button(theSurface)

    def mouse_down(self, theEvent: Event):

        localPosition = theEvent.local

        scrollDownRect: Rect = self.scroll_down_rect()
        scrollUpRect:   Rect = self.scroll_up_rect()

        scrolledDown: bool = scrollDownRect.collidepoint(localPosition[0], localPosition[1])
        scrolledUp: bool = scrollUpRect.collidepoint(localPosition[0], localPosition[1])

        if scrolledDown:
            self.firstIdx += 1
        elif scrolledUp:
            if self.firstIdx != 0:
                self.firstIdx -= 1

        if self.firstRow < 0:
            self.firstIdx = 0
        if self.firstIdx >= len(self.lines) - 1:
            self.firstIdx = len(self.lines) - 1

        # self.firstRow = self.firstIdx
        # self._recomputeTextToDisplayIndices()

        self.logger.debug(f"firstRow: {self.firstRow} -- len(self.lines) {len(self.lines)}")

    def computeBoxSize(self, theNumberOfColumns: int, theNumberOfRows: int) -> tuple:

        width, height = self.font.size(TextBox.CANONICAL_WIDEST_TALLEST_CHARACTER)

        self.logger.debug(f"width: {width}, height: {height}")

        size = (width * theNumberOfColumns, (height * theNumberOfRows) + self.margin)
        self.logger.debug(f"size {size}")

        return size

    def draw_scroll_up_button(self, theSurface: Surface):

        r = self.scroll_up_rect()
        c = self.scroll_button_color
        draw.polygon(theSurface, c, [r.bottomleft, r.midtop, r.bottomright])

    def draw_scroll_down_button(self, theSurface: Surface):

        r = self.scroll_down_rect()
        c = self.scroll_button_color
        draw.polygon(theSurface, c, [r.topleft, r.midbottom, r.topright])

    def scroll_up_rect(self):

        d = self.scroll_button_size
        r = Rect(0, 0, d, d)
        m = self.margin
        r.top = m
        r.right = self.width - m
        r.inflate_ip(-4, -4)
        return r

    def scroll_down_rect(self):

        d = self.scroll_button_size
        r = Rect(0, 0, d, d)
        m = self.margin
        r.bottom = self.height - m
        r.right = self.width - m
        r.inflate_ip(-4, -4)

        return r

    def _recomputeTextToDisplayIndices(self):

        # self.firstIdx = self.firstRow
        if len(self.lines) < self.numberOfRows:
            self.lastIdx = len(self.lines)
        else:
            if self.lastInsertedVisible is True:
                self.lastIdx  = len(self.lines)
                self.firstIdx = self.lastIdx - self.numberOfRows
                self.firstRow = self.firstIdx
            else:
                self.lastIdx = self.firstIdx + self.numberOfRows
                if self.lastIdx >= len(self.lines):
                    self.lastIdx = len(self.lines)
        self.logger.debug(f"firstIdx: {self.firstIdx}  lastIdx: {self.lastIdx}")
