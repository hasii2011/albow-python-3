
import logging

from albow.utils import overridable_property


class DummyVehicle:

    velocity = overridable_property(name='velocity', doc="How fast we are going")
    weight = overridable_property(name='weight', doc="How fat we are")
    width = overridable_property(name='width', doc="How wide our butt is")
    height = overridable_property(name='height', doc="How tall we are not")

    def __init__(self):

        self.logger = logging.getLogger(__name__)

        self._velocity = 0
        self._weight = 0
        self._width = 0
        self._height = 0

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, theNewValue: int):
        self._velocity = theNewValue

    def get_weight(self):
        return self._weight

    def set_weight(self, theNewValue: int):
        self._weight = theNewValue

    def get_width(self):
        return self._width

    def set_width(self, theNewValue: int):
        self._width = theNewValue

    def get_height(self):
        return self._height

    def set_height(self, theNewValue: int):
        self._height = theNewValue

    def __eq__(self, theOtherOne):

        if isinstance(theOtherOne, DummyVehicle):
            if self._velocity == theOtherOne.velocity and \
                    self._weight == theOtherOne.weight and \
                    self._width == theOtherOne.width and \
                    self._height == theOtherOne.height:
                return True
        else:
            return False
