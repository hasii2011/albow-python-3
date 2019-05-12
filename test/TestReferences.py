
import logging

import unittest

from TestBase import TestBase

from albow.References import AttrRef

from DummyControl import DummyControl
from albow.input.IntField import IntField

from TestVehicle import TestVehicle

class TestReferences(TestBase):
    """
    """

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""
        self.logger = logging.getLogger(__name__)

    def testBasicAttrRef(self):

        testVehicle: TestVehicle = TestVehicle()

        velocityRef = AttrRef(base=testVehicle, name="velocity")
        self.logger.info("Created a velocity reference: %s", velocityRef)

        velocityControl: DummyControl = DummyControl(ref=velocityRef)
        self.logger.info("Created velocity control %s", velocityControl)
        #
        # Change the data model
        #
        testVehicle.velocity = 100

        self.assertTrue(velocityControl.get_value() == testVehicle.velocity, "Reference did not update control")

        testVehicle.velocity = 200
        self.assertTrue(velocityControl.get_value() == testVehicle.velocity, "Reference did not update control")
        #
        # Change the control
        #
        velocityControl.set_value(500)
        self.assertTrue(velocityControl.get_value() == testVehicle.velocity, "Control did not update reference")

if __name__ == '__main__':
    unittest.main()
