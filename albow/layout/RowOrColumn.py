
from albow.core.Widget import Widget


class RowOrColumn(Widget):
    """

    """
    axis_anchors = {'w': 'lr', 'h': 'tb'}

    _is_gl_container = True

    d:          tuple = None
    minor_axis: str   = None
    axis:       str   = None
    longways:   str   = None
    crossways:  str   = None
    align_map:  dict  = None

    def __init__(self, size, items, kwds):
        """

        Args:
            size:
            items:
            kwds:
        """
        align    = kwds.pop('align', 'c')
        spacing  = kwds.pop('spacing', 10)
        expand   = kwds.pop('expand', None)
        equalize = kwds.pop('equalize', '')
        if isinstance(expand, int):
            expand = items[expand]
        self.equalize_widgets(items, equalize)
        #
        # Python 3 update
        # Widget.__init__(self, **kwds)
        super().__init__(**kwds)

        d = self.d
        longways = self.longways
        crossways = self.crossways
        axis = self.axis
        k, attr2, attr3 = self.align_map[align]
        w = 0
        length = 0
        if isinstance(expand, int):
            expand = items[expand]
        move = ''
        for item in items:
            r = item.rect
            w = max(w, getattr(r, crossways))
            if item is expand:
                item.set_resizing(axis, 's')
                move = 'm'
            else:
                item.set_resizing(axis, move)
                length += getattr(r, longways)
        if size is not None:
            n = len(items)
            if n > 1:
                length += spacing * (n - 1)
            setattr(expand.rect, longways, max(1, size - length))
        h = w * k // 2
        m = self.margin
        px = h * d[1] + m
        py = h * d[0] + m
        sx = spacing * d[0]
        sy = spacing * d[1]
        for item in items:
            setattr(item.rect, attr2, (px, py))
            self.add(item)
            p = getattr(item.rect, attr3)
            px = p[0] + sx
            py = p[1] + sy
        self.shrink_wrap()

    def equalize_widgets(self, items, mode):
        if items:
            if 'w' in mode:
                s = max(w.width for w in items)
                for w in items:
                    w.width = s
            if 'h' in mode:
                s = max(w.height for w in items)
                for w in items:
                    w.height = s
            if self.minor_axis in mode:
                anchor = self.axis_anchors[self.minor_axis]
                for w in items:
                    w.add_anchor(anchor)
