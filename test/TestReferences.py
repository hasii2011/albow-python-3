
from logging import Logger
from logging import getLogger

from unittest import expectedFailure
from unittest import main as unitTestMain

from test.DummyControl import DummyControl
from test.DummyVehicle import DummyVehicle

from albow.ItemRefInsertionException import ItemRefInsertionException

from albow.References import AttrRef
from albow.References import ItemRef


from test.TestBase import TestBase


TEST_ITEM_INDEX = 3


class TestReferences(TestBase):
    """
    """

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""
        self.logger: Logger = getLogger(__name__)

    def testBasicAttrRef(self):

        testVehicle: DummyVehicle = DummyVehicle()

        velocityRef = AttrRef(base=testVehicle, name="velocity")
        self.logger.info("Created: %s", velocityRef)

        velocityControl: DummyControl = DummyControl(ref=velocityRef)
        self.logger.info("Created: %s", velocityControl)
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

    @expectedFailure
    def testBadItemRefInsertion(self):

        vehicleList = self.getVehicleList()

        itemRef = ItemRef(base=vehicleList, index=TEST_ITEM_INDEX)
        self.logger.info("Created %s", itemRef)

        velocityControl: DummyControl = DummyControl(ref=itemRef)
        self.logger.info("Created velocity control %s", velocityControl)
        #
        # Change the control
        #
        try:
            velocityControl.set_value(500)
            self.assertTrue(velocityControl.get_value() == vehicleList[TEST_ITEM_INDEX].velocity, "Control did not update reference")
        except ItemRefInsertionException as e:
            self.logger.debug(f"{e.message}")
            self.fail('Expected failure')

    def testBasicItemRefRetrieval(self):

        vehicleList = self.getVehicleList()

        itemRef = ItemRef(base=vehicleList, index=TEST_ITEM_INDEX)
        self.logger.info(f"Created {itemRef=}")

        velocityControl: DummyControl = DummyControl(ref=itemRef)
        self.logger.info("Created velocity control %s", velocityControl)

        anItem = itemRef.get()
        self.assertEqual(first=vehicleList[TEST_ITEM_INDEX], second=anItem, msg="Did not retrieve what I put in.")

    def testItemRefIndexing(self):

        vehicleList = self.getVehicleList()

        itemRef = ItemRef(base=vehicleList, index=TEST_ITEM_INDEX)
        self.logger.info("Created: %s", itemRef)

        testItem = itemRef[TEST_ITEM_INDEX]
        self.logger.info("Retrieved: %s", testItem)
        self.assertEqual(first=vehicleList[TEST_ITEM_INDEX], second=testItem, msg="Did not retrieve the correct item.")

    @staticmethod
    def getVehicleList():

        vehicleList = []
        for i in range(0, 5):
            testVehicle: DummyVehicle = DummyVehicle()
            testVehicle.weight = i * 100
            testVehicle.velocity = (i * 2) * 10
            vehicleList.append(testVehicle)

        return vehicleList


if __name__ == '__main__':
    unitTestMain()
