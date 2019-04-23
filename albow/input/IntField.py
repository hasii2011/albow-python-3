
from albow.input.Field import Field

class IntField(Field):

    def __init__(self, width=None, **kwds):
        self.type = int
        super().__init__(width, **kwds)
