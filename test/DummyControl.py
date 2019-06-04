
import logging

from albow.widgets.Control import Control

from albow.themes.ThemeProperty import ThemeProperty


class DummyControl(Control):

    dummyThemeAttribute = ThemeProperty('dummyThemeAttribute')

    """"
    A dummy control for unit testing

    """
    def __init__(self, **attrs):

        self.logger = logging.getLevelName(__name__)
        self.set(**attrs)
        self._dummyThemeAttribute = None

    def getDummyThemeAttribute(self):
        return self._dummyThemeAttribute

    def setDummyThemeAttribute(self, theNewValue):
        self._dummyThemeAttribute = theNewValue

    def set(self, **kwds):

        for name, value in kwds.items():
            if not hasattr(self, name):
                raise TypeError("Unexpected keyword argument '%s'" % name)
            setattr(self, name, value)

    def __repr__(self):
        formattedMe: str = \
            f"DummyControl(value: '{self._value}' enabled: '{self._enabled}' highlighted: '{self._highlighted})'"
        return formattedMe
