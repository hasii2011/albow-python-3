
import logging

from pygame import Surface
from pygame import Rect
from pygame.event import Event

from albow.core.Widget import Widget

from albow.containers.PaletteView import PaletteView

LISTBOX_DEFAULT_ROWS: int  = 10
LISTBOX_COLUMNS:      int  = 1
LISTBOX_SCROLLS:      bool = True


class ListBox(PaletteView):

    """

    """
    client:    Widget = None
    selection: int    = None
    items             = []
    selectAction      = None

    def __init__(self, theClient: Widget, theItems: list, selectAction=None, **kwargs):

        assert isinstance(theItems, list), "Wrong type for input list"

        font = self.predict_font(kwargs)
        h    = font.get_linesize()
        d    = 2 * self.predict(kwargs, 'margin')

        listBoxWidth: int = int(theClient.width / 2)

        cellSize = (listBoxWidth - d, h)

        super().__init__(cell_size=cellSize, nrows=LISTBOX_DEFAULT_ROWS, ncols=LISTBOX_COLUMNS, scrolling=LISTBOX_SCROLLS, **kwargs)

        self.border_width = 1
        self.margin       = 5

        self.client = theClient
        self.items  = theItems
        self.selectAction = selectAction
        self.logger = logging.getLogger(__name__)

    #
    # The 4 methods below implement the PaletteView abstract methods
    #

    def num_items(self) -> int:
        return len(self.items)

    def draw_item(self, theSurface: Surface, theItemNumber: int, theRect: Rect):

        # self.logger.info("draw_item %s ", theRect.size)
        color = self.fg_color
        buf = self.font.render(self.items[theItemNumber], True, color)

        theSurface.blit(buf, theRect)

    def click_item(self, theItemNumber: int, theEvent: Event):

        self.logger.debug("click_item: %s", theItemNumber)

        self.selection = theItemNumber
        if self.selectAction != None:
            self.selectAction(self.items[self.selection])

    def item_is_selected(self, theItemNumber: int) -> bool:

        ans: bool = theItemNumber == self.selection
        return ans
