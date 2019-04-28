
from pygame import Surface

from albow.core.Widget import Widget

class DirectoryPathView(Widget):

    def __init__(self, width, client, **kwds):

        super().__init__(**kwds)
        self.set_size_for_text(width)
        self.client = client

    def draw(self, surface: Surface):

        frame = self.get_margin_rect()
        image = self.font.render(self.client.directory, True, self.fg_color)
        tw = image.get_width()
        mw = frame.width
        if tw <= mw:
            x = 0
        else:
            x = mw - tw
        surface.blit(image, (frame.left + x, frame.top))

