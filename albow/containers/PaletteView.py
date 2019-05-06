
import logging

from pygame import Rect
from pygame import Surface
from pygame import draw

from pygame.event import Event

from albow.containers.GridView import GridView
from albow.utils import frame_rect

from albow.themes.ThemeProperty import ThemeProperty


class PaletteView(GridView):
    """
    The PaletteView class is an abstract base class for implementing tool palettes and similar things. A PaletteView
    displays an array of items which can be selected by clicking, with the selected item being highlighted. There
    is provision for scrolling, so that the palette can contain more items than are displayed at one time.

    The PaletteView does not maintain the items themselves or keep track of which one is selected; these things
    are responsibilities of the subclass.
    """
    """
       nrows   int   No. of displayed rows
       ncols   int   No. of displayed columns

       Abstract methods:

         num_items()  -->  no. of items
         draw_item(surface, item_no, rect)
    """

    sel_width = ThemeProperty('sel_width')
    """
    Width of the border drawn around the selected item when the highlight_style is 'frame'.
    """
    scroll_button_size = ThemeProperty('scroll_button_size')
    """
    Size of the scrolling buttons. (This is a number, not a tuple -- the scroll buttons are square.)
    """
    scroll_button_color = ThemeProperty('scroll_button_color')
    """
    Color in which to draw the scrolling buttons.
    """
    highlight_style = ThemeProperty('highlight_style')
    """
    Determines the way in which a selected cell is highlighted. Values are 'frame' to draw a frame around 
    the cell, 'fill' to fill its background with the sel_color, and 'reverse' to swap the 
    foreground and background colours.
    """

    def __init__(self, cell_size, nrows, ncols, scrolling=False, **kwds):
        """
        Initializes the palette view with the specified cell_size, and a rect sized for displaying
        nrows rows and ncols columns of items. If scrolling is true, controls will be
        displayed for scrolling the view.

        Args:
            cell_size:  A tuple that specifies the cell size (width, height)
            nrows:      The # of rows
            ncols:      The # of columns
            scrolling:  True to display scroll bars, else false
            **kwds:
        """

        self.logger = logging.getLogger(__name__)

        #
        # Python 3 update
        #
        # GridView.__init__(self, cell_size, nrows, ncols, **kwds)
        super().__init__(cell_size, nrows, ncols, **kwds)

        self.scrolling = scrolling
        if scrolling:
            d = self.scroll_button_size
            #l = self.width
            #b = self.height
            self.width += d
        # self.scroll_up_rect = Rect(l, 0, d, d).inflate(-4, -4)
        # self.scroll_down_rect = Rect(l, b - d, d, d).inflate(-4, -4)
        self.scroll = 0

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

    def draw(self, surface):
        GridView.draw(self, surface)
        if self.can_scroll_up():
            self.draw_scroll_up_button(surface)
        if self.can_scroll_down():
            self.draw_scroll_down_button(surface)

    def draw_scroll_up_button(self, surface):
        r = self.scroll_up_rect()
        c = self.scroll_button_color
        draw.polygon(surface, c, [r.bottomleft, r.midtop, r.bottomright])

    def draw_scroll_down_button(self, surface):
        r = self.scroll_down_rect()
        c = self.scroll_button_color
        draw.polygon(surface, c, [r.topleft, r.midbottom, r.topright])

    def draw_cell(self, surface, row, col, rect):
        i = self.cell_to_item_no(row, col)
        if i is not None:
            highlight = self.item_is_selected(i)
            self.draw_item_and_highlight(surface, i, rect, highlight)

    def draw_item_with(self, surface, i, rect, fg):
        old_fg = self.fg_color
        self.fg_color = fg
        try:
            self.draw_item(surface, i, rect)
        finally:
            self.fg_color = old_fg

    def draw_prehighlight_with(self, theSurface: Surface, theItemNumber: int, theRect: Rect, color):

        style = self.highlight_style
        if style == 'frame':
            frame_rect(theSurface, color, theRect, self.sel_width)
        elif style == 'fill' or style == 'reverse':
            theSurface.fill(color, theRect)

    def mouse_down(self, event):

        if self.scrolling:

            p = event.local
            #
            # Python 3 method signature update for tuples
            # break up to make easier to debub
            #
            scrollDownRect: Rect = self.scroll_down_rect()
            scrollUpRect:   Rect = self.scroll_up_rect()
            canScrollDown:  bool = scrollDownRect.collidepoint(p[0], p[1])
            canScrollUp:    bool = scrollUpRect.collidepoint(p[0], p[1])

            self.logger.debug("p: %s, downRect.centerx %s, downRect.centery %s", p, scrollDownRect.centerx,scrollDownRect.centery)

            # if self.scroll_up_rect().collidepoint(p):
            if canScrollUp:
                self.scroll_up()
                return
            # elif self.scroll_down_rect().collidepoint(p):
            elif canScrollDown:
                self.scroll_down()
                return
        GridView.mouse_down(self, event)

    def scroll_up(self):
        if self.can_scroll_up():
            self.scroll -= self.items_per_page()

    def scroll_down(self):
        if self.can_scroll_down():
            self.scroll += self.items_per_page()

    def scroll_to_item(self, n):
        i = max(0, min(n, self.num_items() - 1))
        p = self.items_per_page()
        self.scroll = p * (i // p)

    def can_scroll_up(self):
        return self.scrolling and self.scroll > 0

    def can_scroll_down(self):
        return self.scrolling and self.scroll + self.items_per_page() < self.num_items()

    def items_per_page(self):
        return self.num_rows() * self.num_cols()

    def click_cell(self, row, col, event):
        i = self.cell_to_item_no(row, col)
        if i is not None:
            self.click_item(i, event)

    def cell_to_item_no(self, row, col):
        i = self.scroll + row * self.num_cols() + col
        if 0 <= i < self.num_items():
            return i
        else:
            return None

    def num_rows(self):
        ch = self.cell_size[1]
        if ch:
            return self.height // ch
        else:
            return 0

    def num_cols(self):
        width = self.width
        if self.scrolling:
            width -= self.scroll_button_size
        cw =  self.cell_size[0]
        if cw:
            return width // cw
        else:
            return 0

    # ========================================================================
    #
    #  Abstract methods follow;  Some implemented with default behavior
    #
    # ========================================================================

    def draw_item_and_highlight(self, theSurface: Surface, theItemNumber: int, theRect: Rect, highlight: bool):
        """
        Draws the cell for item theItemNumber, together with highlighting if highlight is true. The default
        implementation calls draw_prehighlight, draw_item and draw_posthighlight.

        Args:
            theSurface:     The surface to drawn on
            theItemNumber:  The item # of highlight
            theRect:        The pygame rect to use
            highlight:      If True highlight

        Returns:

        """
        if highlight:
            self.draw_prehighlight(theSurface, theItemNumber, theRect)
        if highlight and self.highlight_style == 'reverse':
            fg = self.inherited('bg_color') or self.sel_color
        else:
            fg = self.fg_color
        self.draw_item_with(theSurface, theItemNumber, theRect, fg)
        if highlight:
            self.draw_posthighlight(theSurface, theItemNumber, theRect)

    def draw_prehighlight(self, theSurface: Surface, theItemNumber: int, theRect: Rect):
        """
        Called for highlighted cells before draw_item, to draw highlighting that is to appear
        underneath the cell's contents.

        Args:
            theSurface:
            theItemNumber:
            theRect:

        """

        if self.highlight_style == 'reverse':
            color = self.fg_color
        else:
            color = self.sel_color
        self.draw_prehighlight_with(theSurface, theItemNumber, theRect, color)

    def draw_posthighlight(self, theSurface: Surface, theItemNumber: int, theRect: Rect):
        """
        Called for highlighted cells after draw_item, to draw highlighting that is to appear
        on top of the cell's contents.

        Args:
            theSurface:
            theItemNumber:
            theRect:

        """
        pass

    def item_is_selected(self, theItemNumber: int) -> bool:
        """
        Should return a boolean indicating whether item number item_no is currently to be considered selected.

        Args:
            theItemNumber:

        Returns True if it is, False
        """

        return False

    def click_item(self, theItemNumber: int, theEvent: Event):
        """
        Called when a mouse-down event occurs in item theItemNumber. Typically the subclass will record the fact that
        the item is selected so that this can be reported later via item_is_selected().

        Args:
            theItemNumber:
            theEvent:

        Returns:

        """
        pass
