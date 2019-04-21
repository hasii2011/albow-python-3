#---------------------------------------------------------------------------
#
#   Albow - Layout widgets
#
#---------------------------------------------------------------------------


from albow.layouts.RowOrColumn import RowOrColumn

class Row(RowOrColumn):

    d          = (1, 0)
    axis       = 'h'
    minor_axis = 'h'
    longways   = 'width'
    crossways  = 'height'
    align_map = {
        't': (0, 'topleft', 'topright'),
        'c': (1, 'midleft', 'midright'),
        'b': (2, 'bottomleft', 'bottomright'),
    }

    def __init__(self, items, width=None, **kwds):
        """
        Row(items, align = alignment, spacing = 10, width = None, expand = None)
        align = 't', 'c' or 'b'
        """
        # Python 3 update
        #
        # RowOrColumn.__init__(self, width, items, kwds)
        super().__init__(width, items, kwds)

class Column(RowOrColumn):

    d          = (0, 1)
    axis       = 'v'
    minor_axis = 'w'
    longways   = 'height'
    crossways  = 'width'
    align_map = {
        'l': (0, 'topleft',  'bottomleft'),
        'c': (1, 'midtop',   'midbottom'),
        'r': (2, 'topright', 'bottomright'),
    }

    def __init__(self, items, height=None, **kwds):
        """
        Column(items, align = alignment, spacing = 10, height = None, expand = None)
        align = 'l', 'c' or 'r'
        """
        # Python 3 update
        #
        # RowOrColumn.__init__(self, height, items, kwds)
        super().__init__(height, items, kwds)
