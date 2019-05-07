
from typing import List

from albow.core.Widget import Widget
from albow.layout.RowOrColumn import RowOrColumn


class Column(RowOrColumn):
    """
    A Column is a container widget that arranges its contents in a vertical column. In an
    OpenGL window, it may contain 3D subwidgets.

    .. Note::
        The layout is only performed when the widget is initially created; it is not updated if you add or remove
        widgets later or change their sizes.
    """
    def __init__(self, items: List[Widget], height=None, **kwds):
        """

        Specify the following as keyword: value pairs in kwds

        - align:
            The widgets in items are added as subwidgets and arranged vertically with spacing pixels between.
            Horizontal alignment is controlled by align, which is one of 'l', 'c' or 'r' for left, centre or right.

        - spacing:  The spacing between the widgets in pixels

        - equalize:
            If equalize contains 'w', the widths of all the items are made equal to the widest one, and 'lr' is
            added to their anchor properties. If equalize contains 'h', the heights of all the items are
            made equal to the tallest one.

        - expand:  The index of the widget in the items list


        Args:
            items:  The widgets to add as items

            height: If a height is specified, then expand may be a widget or an index into the items, and the specified
                    widget has its height adjusted to fill the remaining space. Otherwise, the initial size of the
                    Column is calculated from its contents.

            **kwds:
        """
        self.d          = (0, 1)
        self.minor_axis = 'w'
        self.axis       = 'v'
        self.longways   = 'height'
        self.crossways  = 'width'
        self.align_map = {
            'l': (0, 'topleft',  'bottomleft'),
            'c': (1, 'midtop',   'midbottom'),
            'r': (2, 'topright', 'bottomright'),
        }

        super().__init__(height, items, kwds)
