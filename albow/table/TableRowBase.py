
from pygame import Rect

from albow.containers.PaletteView import PaletteView


class TableRowBase(PaletteView):

    def __init__(self, cell_size, nrows, scrolling, **kwds):
        """

        :param cell_size:
        :param nrows:
        :param scrolling:
        """
        #
        # Python 3 update
        #
        # PaletteView.__init__(self, cell_size, nrows, 1, scrolling=scrolling)
        super().__init__(cell_size, nrows, 1, scrolling=scrolling, **kwds)

    def num_items(self):
        return self.parent.num_rows()

    def draw_item(self, surf, row, row_rect):
        table = self.parent
        height = row_rect.height
        row_data = self.row_data(row)
        for i, x, width, column, cell_data in table.column_info(row_data):
            cell_rect = Rect(x, row_rect.top, width, height)
            self.draw_table_cell(surf, cell_data, cell_rect, column)

    def row_data(self, row):
        return self.parent.row_data(row)

    def draw_table_cell(self, surf, data, cell_rect, column):
        self.parent.draw_table_cell(surf, data, cell_rect, column)
