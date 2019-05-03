
from albow.layout.Column import Column
from albow.utils import blit_in_rect

from albow.table.TableHeaderView import TableHeaderView
from albow.table.TableRowView import TableRowView


class TableView(Column):

    columns = []
    header_font = None
    header_fg_color = None
    header_bg_color = None
    header_spacing = 5
    column_margin = 2

    def __init__(self, nrows=None, height=None, header_height=None, row_height=None, scrolling=True, **kwds):
        """

        :param nrows:
        :param height:
        :param header_height:
        :param row_height:
        :param scrolling:
        :param kwds:
        """
        columns = self.predict_attr(kwds, 'columns')
        if row_height is None:
            font = self.predict_font(kwds)
            row_height = font.get_linesize()
        if header_height is None:
            header_height = row_height
        row_width = 0
        if columns:
            for column in columns:
                row_width += column.width
            row_width += 2 * self.column_margin * len(columns)
        contents = []
        header = None
        if header_height:
            header = TableHeaderView(row_width, header_height)
            contents.append(header)
        row_size = (row_width, row_height)
        if not nrows and height:
            nrows = height // row_height
        rows = TableRowView(row_size, nrows or 10, scrolling=scrolling)
        contents.append(rows)
        s = self.header_spacing
        #
        # Python 3 update
        #
        # Column.__init__(self, contents, align = 'l', spacing = s, **kwds)
        super().__init__(contents, align='l', spacing=s, **kwds)
        if header:
            header.font = self.header_font or self.font
            header.fg_color = fg_color = self.header_fg_color or self.fg_color
            header.bg_color = bg_color = self.header_bg_color or self.bg_color
        rows.font = self.font
        rows.fg_color = self.fg_color
        rows.bg_color = self.bg_color
        rows.sel_color = self.sel_color

    def column_info(self, row_data):
        columns = self.columns
        m = self.column_margin
        d = 2 * m
        x = 0
        for i, column in enumerate(columns):
            width = column.width
            if row_data:
                data = row_data[i]
            else:
                data = None
            yield i, x + m, width - d, column, data
            x += width

    def draw_header_cell(self, surf, i, cell_rect, column):
        self.draw_text_cell(surf, i, column.title, cell_rect, column.alignment, self.font)

    def draw_table_cell(self, surf, i, data, cell_rect, column):
        text = column.format(data)
        self.draw_text_cell(surf, i, text, cell_rect, column.alignment, self.font)

    def draw_text_cell(self, surf, i, data, cell_rect, align, font):
        buf = font.render(str(data), True, self.fg_color)
        blit_in_rect(surf, buf, cell_rect, align)

    def row_is_selected(self, n):
        return False

    def click_row(self, n, e):
        pass
