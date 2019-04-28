

class AttrRef:
    """
    AttrRef is here for backwards compatibility.
    New code should use references.Ref instead.
    """

    def __init__(self, obj, attr):
        self.obj = obj
        self.attr = attr

    def get(self):
        return getattr(self.obj, self.attr)

    def set(self, x):
        setattr(self.obj, self.attr, x)


class ItemRef:
    """
    ItemRef is here for backwards compatibility.
    New code should use references.Ref instead.
    """

    def __init__(self, obj, item):
        self.obj  = obj
        self.item = item

    def get(self):
        # return self.obj[item]
        return self.obj[self.item]   # Python 3 update

    def set(self, x):
        # self.obj[item] = x
        self.obj[self.item] = x     # Python 3 update
