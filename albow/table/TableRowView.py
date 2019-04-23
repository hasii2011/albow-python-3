from pygame import event

from albow.table.TableRowBase import TableRowBase


class TableRowView(TableRowBase):

    highlight_style = 'fill'
    vstretch = True

    #
    # Python 3 update to make sure scrolling values get passed through
    #
    def __init__(self, cellSize: tuple, nRows: int, scrolling: bool):
        super().__init__(cellSize, nRows, scrolling)

    def item_is_selected(self, n: int):
        return self.parent.row_is_selected(n)

    def click_item(self, n: int, e: event):
        self.parent.click_row(n, e)
