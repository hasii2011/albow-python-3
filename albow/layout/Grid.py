
from logging import Logger
from logging import getLogger

from pygame import Rect

from albow.core.ui.Widget import Widget


DEFAULT_GRID_COLUMN_SPACING = 10
DEFAULT_GRID_ROW_SPACING    = 10
DEFAULT_GRID_MARGIN         = 3


class Grid(Widget):

    _is_gl_container = True
    margin = 0

    def __init__(self, rows, row_spacing=DEFAULT_GRID_ROW_SPACING, column_spacing=DEFAULT_GRID_COLUMN_SPACING, **kwds):

        self.logger: Logger = getLogger(__name__)

        self.margin = m = kwds.pop('margin', self.margin)
        if self.margin == 0:
            self.margin = DEFAULT_GRID_MARGIN
            m           = DEFAULT_GRID_MARGIN

        self.logger.debug(f'margin: {self.margin}')
        col_widths  = [0] * len(rows[0])
        row_heights = [0] * len(rows)
        for j, row in enumerate(rows):
            for i, widget in enumerate(row):
                if widget:
                    col_widths[i]  = max(col_widths[i], widget.width)
                    row_heights[j] = max(row_heights[j], widget.height)

        self.logger.debug(f"column_spacing: {column_spacing}")
        self.logger.debug(f"... col_widths: {col_widths} ... row_heights: {row_heights}")

        row_top:  int = 0
        col_left: int = 0
        for j, row in enumerate(rows):
            h = row_heights[j]
            y = m + row_top + h // 2

            col_left = 0
            for i, widget in enumerate(row):
                w = col_widths[i]
                if widget:
                    if i == 0:
                        x = m + col_left
                        self.logger.debug(f"x: {x} m: {m} + col_left: {col_left}")
                    else:
                        x = column_spacing + col_left
                        self.logger.debug(f"x: {x} column_spacing: {column_spacing} + col_left: {col_left}")

                    widget.midleft = (x, y)
                    self.logger.debug(f'widget.midleft: {widget.midleft}')
                col_left += w + column_spacing
            row_top += h + row_spacing
        #
        # Bad warning on "local variable col_left might be referenced before assignment"
        #
        width  = max(1, col_left - column_spacing)
        height = max(1, row_top - row_spacing)
        m2 = 2 * m
        self.logger.debug(f"width: '{width}'  m2: '{m2}' column_spacing: '{column_spacing}' height: '{height}' #cols: {len(col_widths)}")
        realWidth: int = width + m2 + (column_spacing * (len(col_widths) - 1))
        r = Rect(0, 0, realWidth, height + m2)

        self.logger.debug(f"r = {r}")

        super().__init__(r, **kwds)
        self.add(rows)

    def __repr__(self):
        return self.__class__.__name__
