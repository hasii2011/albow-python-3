

from pygame.color import Color

from albow.containers.PaletteView import PaletteView


class DemoPaletteView(PaletteView):
    """
    Palette View
    """

    info = ["red", "green", "blue", "cyan", "magenta", "yellow"]

    sel_color = Color("white")
    sel_width = 5

    def __init__(self):

        super().__init__((60, 60), 2, 2, scrolling=True)
        self.selection = None
        self.border_width = 1

    def num_items(self):
        return len(self.info)

    def draw_item(self, surface, item_no, rect):

        inflationSize = -2 * self.sel_width
        r = rect.inflate(inflationSize, inflationSize)
        color = Color(self.info[item_no])
        surface.fill(color, r)

    def click_item(self, item_no, theEvent):
        self.selection = item_no

    def item_is_selected(self, item_no):
        return self.selection == item_no
