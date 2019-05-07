
from pygame import font
from pygame import Surface
from pygame import Rect

from pygame.event import Event

from albow.layout.Column import Column
from albow.utils import blit_in_rect

from albow.table.TableHeaderView import TableHeaderView
from albow.table.TableRowView import TableRowView
from albow.table.TableColumn import TableColumn


class TableView(Column):
    """
    A TableView provides a tabular view of data having a fixed number of columns and a variable number of rows. There
    may be a header providing titles for the columns. There is provision for scrolling and for allowing the user
    to select rows.

    An auxiliary class TableColumn is used to configure the formatting of the headers and data.

    By default, all headers and data are displayed textually, but this can be changed by overriding methods
    of the TableView.
    """
    columns: TableColumn = []
    """
    A list of TableColumn instances describing the columns of the table.
    """
    header_font: font = None
    """
    Font in which to display the column headers.
    """
    header_fg_color = None
    """
    Foreground colour of the column headers.
    """
    header_bg_color = None
    """
    Background colour of the column headers, or None.
    """
    header_spacing = 5
    """
    Space to leave between the header and the rows.  Default is 5 pixels
    """
    column_margin = 2
    """
    Space to leave either side of the contents of a column. Default is 2 pixels
    """

    def __init__(self, nrows=None, theHeight=None, header_height=None, row_height=None, scrolling=True, **kwds):
        """

        The TableView is initialized with a width and height determined as follows:

        - The initial width is calculated from the information in the *columns* attribute.
        - The initial height, excluding the header, is determined either directly by the height parameter or by the
          row height and number of rows *nrows*. If no *row_height* is specified, it is calculated from the size of
          the font.
        - The height of the header is determined by ''header_height'', or the size of the header font.


        Args:
            nrows:  The # of rows

            theHeight:

            header_height: If None use the size of the header font

            row_height:

            scrolling:   If scrolling is true, the table will display scrolling arrows.

            **kwds:
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

        if not nrows and theHeight:
            nrows = theHeight // row_height
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

    def draw_header_cell(self, theSurface: Surface, cell_rect: Rect, theTableColumn: TableColumn):
        """
        Draws the header of TableColumn
        By default, the column's title is displayed
        using the header_font and the alignment specified by coldesc.
        Args:
            theSurface:       The pygame surface to use

            cell_rect: The rect is the rectangle corresponding to the header area,

            theTableColumn:  The table column header to render

        """
        self.draw_text_cell(theSurface, theTableColumn.title, cell_rect, theTableColumn.alignment, self.font)

    def draw_table_cell(self, surf: Surface, data: str, cell_rect: Rect, tableColumn: TableColumn):
        """
        Draws a cell of the table. data is the data item to be displayed, rect is the rectangle corresponding to the
        cell, By default, the data is formatted as
        specified by TableColumn's format_string and rendered using the widget's font.

        Args:
            surf:       The pygame Surface

            data:   The data to display

            cell_rect: The rect is the rectangle corresponding to the header area,

            theTableColumn:  The table column header to render
        """
        text = tableColumn.format(data)
        self.draw_text_cell(surf, text, cell_rect, tableColumn.alignment, self.font)

    def draw_text_cell(self, theSurface: Surface, data, cell_rect: Rect, align: str, theFont: font):
        """

        Args:
            theSurface:
            data:
            cell_rect:
            align:
            theFont:

        """

        buf: Surface = theFont.render(str(data), True, self.fg_color)
        blit_in_rect(theSurface, buf, cell_rect, align)

    #
    #  Abstract methods follow
    #
    def click_row(self, theRowNumber: int, theEvent: Event):
        """
        Called when theRowNumber is clicked. The default implementation does nothing.

        Args:
            theRowNumber: The 'clicked' row number

            theEvent:  The associated event

        """
        pass

    def row_is_selected(self, theRowNumber: int, theEvent: Event) -> bool:
        """
        Should return true if *theRowNumber* is considered selected. The default implementation
        always returns *False*.  *StarStar*, 'quotequote'
        Args:
            theRowNumber:  The selected row number to check

            theEvent:  The associated pygame event

        Returns: *True* if selected, else *False*

        """
        return False

    def num_rows(self) -> int:
        """

        Returns:  The # of rows
        """
        pass

    def row_data(self, theRowNumber: int):
        """

        Should return a sequence of data items for row number n. The data items may be of any type, provided they
        can be formatted as specified by the corresponding TableColumn. Must be implemented.

        Args:
            theRowNumber: A row number

        Returns:  Row data

        """
        pass
