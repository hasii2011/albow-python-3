
from albow.widget import Widget


class Frame(Widget):
    #  margin  int

    border_width: int = 1
    margin:       int = 2   # spacing between border and widget

    def __init__(self, client, border_spacing=None, **kwds):

        super().__init__(**kwds)

        self.client = client
        if border_spacing is not None:
            self.margin = self.border_width + border_spacing
        d = self.margin
        w, h = client.size
        self.size = (w + 2 * d, h + 2 * d)
        client.topleft = (d, d)
        self.add(client)
