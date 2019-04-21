
from albow.layouts.RowOrColumn import RowOrColumn


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
