
from albow.widgets.Control import Control

from albow.input.TextEditor import TextEditor


class Field(Control, TextEditor):

    """
    Field is an abstract base class for controls that edit a value with a textual representation. It provides
    facilities for

    - Converting between the text and internal representations of the value,
    - For specifying minimum and maximum allowed values, and
    - Controlling whether the value is allowed to be empty and what representation to use for an empty value.

    A Field can be in two states, _editing_ and _non-editing_. In the non-editing state, the control displays
    the value to which it is linked via its `ref` attribute. When the user focuses the control and begins typing,
    it switches to the editing state. In this state, the text may be edited but the associated value is not yet
    updated. When the `Return`, `Enter` or `Tab key` is pressed, or a mouse click occurs anywhere outside the field,
    the value is updated and the control returns to the non-editing state. Updating of the value can also be
    forced by calling the `commit()` method.
    """

    empty = NotImplemented
    """
    Internal value to use when the field is empty.  If set to NotImplemented, the user is not allowed to enter 
    an empty value.
    """
    format = "%s"
    """
    Format string to use when converting the internal representation to text. See also format_value() below.
    """
    min: int = None
    """
    Minimum allowable value.  If `None`, no minimum value will be enforced.
    """
    max: int = None
    """
    Maximum allowable value.  If `None`, no maximum value will be enforced.
    """
    type = None
    """
    A function for converting from text to the internal representation.  Typically a type object, but 
    can be any callable object.
    """
    editing: bool = None
    """
    _Read only_. A boolean which is true when the control is in the editing state.
    """
    insertion_point = None

    def __init__(self, width=None, **kwds):
        """

        Args:
            width:  The width may be an integer or a string, as for TextEditor. If no width is specified, but a
                    value for min and/or max is specified at construction time, the width will be determined from
                    the min or max value. If no other way of determining the width is available, it defaults to 100.

            **kwds:
        """
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

    def format_value(self, theValueToFormat):
        """
        This method is called to format the value for display. By default it uses the format string specified by
        the format attribute. You can override this method to format the value in a different way.

        Args:
            theValueToFormat:  The value

        Returns:  The formatted value

        """
        if theValueToFormat == self.empty:
            return ""
        else:
            return self.format % theValueToFormat

    def get_text(self):
        if self.editing:
            return self._text
        else:
            return self.format_value(self.value)

    def set_text(self, theNewText):
        self.editing = True
        self._text = theNewText

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
        """
        When in the editing state, causes the control's value to be updated and places the control
        in the non-editing state.
        """
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
