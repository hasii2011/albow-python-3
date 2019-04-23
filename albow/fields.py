#
#   Albow - Fields
#

from albow.input.Field import Field


class TextField(Field):

    _value = ""

    def __init__(self, width=None, **kwds):
        self.type = str
        super().__init__(width, **kwds)


class IntField(Field):

    def __init__(self, width=None, **kwds):
        self.type = int
        super().__init__(width, **kwds)


class FloatField(Field):

    def __init__(self, width=None, **kwds):
        self.type = float
        super().__init__(width, **kwds)
