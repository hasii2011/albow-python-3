
from albow.table.TableRowBase import TableRowBase


class TableHeaderView(TableRowBase):

    def __init__(self, width, height):
        super().__init__((width, height), 1, False)

    def row_data(self, row):
        pass

    def draw_table_cell(self, surf, data, cell_rect, column):
        self.parent.draw_header_cell(surf, cell_rect, column)
