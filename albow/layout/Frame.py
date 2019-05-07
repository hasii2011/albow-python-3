
from albow.core.Widget import Widget


class Frame(Widget):
    """
    A Frame is a container widget that adds a border around a client widget at a specified distance.
    """

    border_width: int = 1
    """
    The width of the border
    """
    margin:       int = 2
    """
    The spacing between border and widget
    """

    def __init__(self, client: Widget, border_spacing: int=None, **kwds):
        """

        Args:
            client:  The widget to wrap

            border_spacing:  Distance between the edges of the client and the border line.

            **kwds:
        """
        super().__init__(**kwds)

        self.client = client
        if border_spacing is not None:
            self.margin = self.border_width + border_spacing
        d = self.margin
        w, h = client.size
        self.size = (w + 2 * d, h + 2 * d)
        client.topleft = (d, d)
        self.add(client)
