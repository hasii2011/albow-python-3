
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


class Column(RowOrColumn):

    def __init__(self, items, height=None, **kwds):
        """

        :param items:
        :param height:
        :param kwds:
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

