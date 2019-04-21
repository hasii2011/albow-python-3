
from albow.layouts.RowOrColumn import RowOrColumn


class Row(RowOrColumn):

    def __init__(self, items, width=None, **kwds):
        """

        :param items:
        :param width:
        :param kwds:
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
