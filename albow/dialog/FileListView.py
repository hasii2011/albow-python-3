
import os

from pygame import Surface
from pygame import Rect

from albow.containers.PaletteView import PaletteView
from albow.dialog.DialogUtilities import alert


class FileListView(PaletteView):

    def __init__(self, width, client, **kwds):
        """

        :param width:
        :param client:
        :param kwds:
        """
        font = self.predict_font(kwds)
        h = font.get_linesize()
        d = 2 * self.predict(kwds, 'margin')
        super().__init__((width - d, h), 10, 1, scrolling=True, **kwds)
        self.client = client
        self.selection = None
        self.names = []

    def update(self):
        client    = self.client
        directory = client.directory

        def aFilter(name):
            path = os.path.join(directory, name)
            return os.path.isdir(path) or self.client.filter(path)

        try:
            names = [name for name in os.listdir(directory)
                     if not name.startswith(".") and aFilter(name)]
        except EnvironmentError as e:
            alert("%s: %s" % (directory, e))
            names = []
        self.names = names
        self.selection = None

    def num_items(self):
        return len(self.names)

    def draw_item(self, surface: Surface, item_no: int, rect: Rect):

        color = self.fg_color
        buf = self.font.render(self.names[item_no], True, color)
        surface.blit(buf, rect)

    def click_item(self, item_no, e):
        self.selection = item_no
        self.client.dir_box_click(e.num_clicks == 2)

    def item_is_selected(self, item_no):
        return item_no == self.selection

    def get_selected_name(self):
        sel = self.selection
        if sel is not None:
            return self.names[sel]
        else:
            return ""

