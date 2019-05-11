
from albow.utils import overridable_property


class Control():
    """
    Control is a mixin class for use by widgets that display and/or edit a value of some kind. It provides a value
    property that can be linked, via a reference object, to a specific attribute or item of another object.
    Reading and writing the value property then accesses the specified attribute or item.

    If no such linkage is specified, a value is kept internally to the Control instance, and
    the value property accesses this internal value. Thus, a Control-based widget can be used stand-alone if desired.

    """
    highlighted = overridable_property('highlighted')
    """
    True if the button should be displayed in a highlighted state. This attribute is maintained by the 
    default mouse handlers.
    """
    enabled = overridable_property('enabled')
    """
    A boolean indicating whether the control is enabled. Defaults to True. By default, this property is 
    read-write and maintains 
    its own state internal to the object. When an enable function is provided, this property becomes 
    read-only and gets its value via the supplied function.
    """
    value = overridable_property('value')
    """
    The current value of the Control. If a ref has been supplied, accesses the value that it specifies. Otherwise, 
    accesses a value stored internally in a private attribute of the Control.
    """

    enable = None
    """
    A function with no arguments that returns a boolean indicating whether the button should be enabled. 
    May also be defined as a method in the subclass.
    """
    ref = None
    """
    Reference to an external value. If supplied, it should be a reference object or other object providing 
    the following methods:
    
        get()
            Should return the current value.

        set(x)
            Should set the value to x.
    """
    _highlighted: bool = False
    _enabled:     bool = True
    _value             = None

    def get_value(self):
        ref = self.ref
        if ref:
            return ref.get()
        else:
            return self._value

    def set_value(self, x):
        ref = self.ref
        if ref:
            ref.set(x)
        else:
            self._value = x
