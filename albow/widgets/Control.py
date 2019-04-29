
from albow.core.Widget import overridable_property

class Control():
    """
        Albow base control

    """

    highlighted = overridable_property('highlighted')
    enabled     = overridable_property('enabled')
    value       = overridable_property('value')

    enable              = None
    ref                 = None
    _highlighted: bool  = False
    _enabled:     bool  = True
    _value              = None

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
