from albow.input.Field import Field


class TextField(Field):

    _value = ""

    def __init__(self, width=None, **kwds):
        self.type = str
        super().__init__(width, **kwds)
