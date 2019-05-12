
import logging

from albow.utils import overridable_property

class TestVehicle:

    velocity = overridable_property(name='velocity', doc="How fast we are going")
    weight = overridable_property(name='weight', doc="How fat we are")
    # width = overridable_property(name='width', doc="How wide our butt is")
    # height = overridable_property(name='height', doc="How tall we are not")
    def __init__(self):

        logger = logging.getLogger(__name__)

        self._velocity = 0
        self._weight = 0
        # self.width = 0
        # self.height = 0

    def get_velocity(self):
        return self._velocity

    def set_velocity(self, theNewValue: int):
        self._velocity = theNewValue

    def get_weight(self):
        return self._weight

    def set_weight(self, theNewValue: int):
        self._weight = theNewValue