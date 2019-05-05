
from pygame import Rect
from pygame import Surface

from pygame.event import Event

from albow.core.Widget import Widget


class GridView(Widget):
    """
    The GridView class is an abstract base class for widgets that display information in a regular grid of
    rows and columns. Subclasses implement methods that define the size of the grid, for drawing a cell of
    the grid and for responding to mouse clicks in a cell.
    """

    def __init__(self, cell_size, nrows, ncols, **kwds):
        """
        Initializes the grid view with the specified cell_size, and a rect sized to show nrows rows and ncols
        columns of cells.

        Note that nrows and ncols are used only for calculating the initial size of the widget, and are not stored.

        Args:
            cell_size:  The cell_size as a tuple (width, height)

            nrows:  The # of rows

            ncols:  The number of columns

            **kwds: Additional property values in keyword:value format

        """
        #
        # Python 3 update
        #
        super().__init__(**kwds)
        self.cell_size = cell_size
        w, h = cell_size
        d = 2 * self.margin
        self.size = (w * ncols + d, h * nrows + d)
        self.cell_size = cell_size

    def draw(self, surface):
        #        for row in xrange(self.num_rows()):
        #            for col in xrange(self.num_cols()):
        #       Python 3 update
        for row in range(self.num_rows()):
            for col in range(self.num_cols()):
                r = self.cell_rect(row, col)
                self.draw_cell(surface, row, col, r)

    def cell_rect(self, theRow: int, theColumn: int) -> Rect:
        """
        Returns a rectangle covering the cell for row 'theRow' and column 'theColumn'.

        Args:
            theRow: The Row

            theColumn: The column

        Returns:    A pygame rectangle

        """
        w, h = self.cell_size
        d = self.margin
        x = theColumn * w + d
        y = theRow * h + d

        return Rect(x, y, w, h)

    def mouse_down(self, event):

        x, y = event.local
        w, h = self.cell_size
        W, H = self.size
        d = self.margin
        if d <= x < W - d and d <= y < H - d:
            row = (y - d) // h
            col = (x - d) // w
            self.click_cell(row, col, event)

    #
    # Abstract methods follow
    #

    def click_cell(self, theRow: int, theColumn: int, theEvent: Event):
        pass

    def draw_cell(self, theSurface: Surface, theRow: int, theColumn: int, rect: Rect):
        pass

    def num_rows(self) -> int:
        """

        Returns:  The # of rows
        """
        pass

    def num_cols(self) -> int:
        """

        Returns: The # of columns
        """
        pass
