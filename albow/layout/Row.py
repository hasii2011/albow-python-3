
from typing import List

from albow.core.Widget import Widget

from albow.layout.RowOrColumn import RowOrColumn


class Row(RowOrColumn):
    """
    A Row is a container widget that arranges its contents in a horizontal row. In an OpenGL window,
    it may contain 3D subwidgets.

    .. Note::
        The layout is only performed when the widget is initially created; it is not updated if you add or remove
        widgets later or change their sizes.

    """
    def __init__(self, items: List[Widget], width=None, **kwds):
        """

        Args:
            items:  The widgets to add as items

            width:  If a width is specified, then expand may be a widget or an index into the items, and the
            specified widget has its width adjusted to fill the remaining space. Otherwise, the initial size
            of the Row is calculated from its contents.

            **kwds:
        """
        self.d          = (1, 0)
        self.minor_axis = 'h'
        self.axis       = 'h'
        self.longways   = 'width'
        self.crossways  = 'height'
        self.align_map = {
                't': (0, 'topleft', 'topright'),
                'c': (1, 'midleft', 'midright'),
                'b': (2, 'bottomleft', 'bottomright'),
        }

        super().__init__(width, items, kwds)
