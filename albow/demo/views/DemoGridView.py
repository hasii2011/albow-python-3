

from pygame.color import Color

from albow.themes.Theme import Theme
from albow.containers.GridView import GridView

DEMO_NCOLS = 3
DEMO_NROWS = 2
DEMO_CELL_WIDTH        = 60
DEMO_CELL_HEIGHT       = 40
DEMO_NUMBER_OF_COLUMNS = 3
DEMO_NUMBER_OF_ROWS    = 2


class DemoGridView(GridView):
    """
    Grid View
    """

    info = [
        [("red", "r3d"), ("green", "gr33n"), ("blue", "blu3")],
        [("cyan", "cy4n"), ("magenta", "m4g3nt4"), ("yellow", "y3ll0w")]
    ]

    def __init__(self):
        """

        """
        attrs = {'bg_color': Theme.WHITE}
        #
        # Python 3 update
        #
        # GridView.__init__(self, (30, 30), 2, 3)
        super().__init__((DEMO_CELL_WIDTH, DEMO_CELL_HEIGHT), DEMO_NROWS, DEMO_NCOLS, **attrs)

    def num_rows(self):
        return DEMO_NUMBER_OF_ROWS

    def num_cols(self):
        return DEMO_NUMBER_OF_COLUMNS

    def draw_cell(self, surface, row, col, rect):
        color = Color(self.info[row][col][0])
        surface.fill(color, rect)

    def click_cell(self, row, col, event):
        self.output.text = self.info[row][col][1]
