
from pygame import Rect

from albow.core.Widget import Widget


DEFAULT_GRID_COLUMN_SPACING = 10
DEFAULT_GRID_ROW_SPACING    = 10


class Grid(Widget):

    _is_gl_container = True
    margin = 0

    def __init__(self, rows, row_spacing=DEFAULT_GRID_ROW_SPACING, column_spacing=DEFAULT_GRID_COLUMN_SPACING, **kwds):

        self.margin = m = kwds.pop('margin', self.margin)
        col_widths = [0] * len(rows[0])
        row_heights = [0] * len(rows)
        for j, row in enumerate(rows):
            for i, widget in enumerate(row):
                if widget:
                    col_widths[i] = max(col_widths[i], widget.width)
                    row_heights[j] = max(row_heights[j], widget.height)

        row_top = 0

        for j, row in enumerate(rows):
            h = row_heights[j]
            y = m + row_top + h // 2
            col_left = 0

            for i, widget in enumerate(row):
                w = col_widths[i]
                if widget:
                    x = m + col_left
                    widget.midleft = (x, y)
                col_left += w + column_spacing
            row_top += h + row_spacing
        #
        # Bad warning on "local variable col_left might be referenced before assignment"
        #
        width = max(1, col_left - column_spacing)
        height = max(1, row_top - row_spacing)
        m2 = 2 * m
        r = Rect(0, 0, width + m2, height + m2)
        #
        # print "albow.controls.Grid: r =", r
        # print "...col_widths =", col_widths
        # print "...row_heights =", row_heights
        #
        super().__init__(r, **kwds)
        self.add(rows)
