
from albow.input.Field import Field


class FloatField(Field):

    def __init__(self, width=None, **kwds):
        self.type = float
        super().__init__(width, **kwds)
