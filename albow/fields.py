#
#   Albow - Fields
#

from albow.widgets.Control import Control
from albow.input.TextEditor import TextEditor


class Field(Control, TextEditor):
    #  type      func(string) -> value
    #  editing   boolean

    empty  = NotImplemented
    format = "%s"
    min    = None
    max    = None
    type   = None

    def __init__(self, width=None, **kwds):

        minimum = self.predict_attr(kwds, 'min')
        maximum = self.predict_attr(kwds, 'max')
        if 'format' in kwds:
            self.format = kwds.pop('format')
        if 'empty' in kwds:
            self.empty = kwds.pop('empty')
        self.editing = False
        if width is None:
            w1 = w2 = ""
            if minimum is not None:
                w1 = self.format_value(minimum)
            if maximum is not None:
                w2 = self.format_value(maximum)
            if w2:
                if len(w1) > len(w2):
                    width = w1
                else:
                    width = w2
        if width is None:
            width = 100
        TextEditor.__init__(self, width, **kwds)

    def format_value(self, x):
        if x == self.empty:
            return ""
        else:
            return self.format % x

    def get_text(self):
        if self.editing:
            return self._text
        else:
            return self.format_value(self.value)

    def set_text(self, text):
        self.editing = True
        self._text = text

    def enter_action(self):
        if self.editing:
            self.commit()
        return 'pass'

    def escape_action(self):
        if self.editing:
            self.editing = False
            self.insertion_point = None
        else:
            return 'pass'

    def attention_lost(self):
        self.commit()

    def commit(self):
        if self.editing:
            text = self._text
            if text:
                try:
                    value = self.type(text)
                except ValueError:
                    return
                if self.min is not None:
                    value = max(self.min, value)
                if self.max is not None:
                    value = min(self.max, value)
            else:
                value = self.empty
                if value is NotImplemented:
                    return
            self.value = value
            self.editing = False
            self.insertion_point = None
        else:
            self.insertion_point = None


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
