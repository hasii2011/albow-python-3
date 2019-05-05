from albow.input.Field import Field


class TextField(Field):

    """
    A control for editing values of type str.

    """
    _value = ""

    def __init__(self, width=None, **kwds):
        self.type = str
        super().__init__(width, **kwds)
