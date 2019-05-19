
import logging
from logging import Logger

import unittest

from TestBase import TestBase

from DummyControl import DummyControl


class TestThemeProperty(TestBase):

    classLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""
        TestThemeProperty.classLogger = logging.getLogger(__name__)

    def tearDown(self):
        """
        cleanup
        """

    def testBaseThemeProperty(self):

        dummyControl: DummyControl = DummyControl()
        dummyControl.setDummyThemeAttribute(42.0)

        themeVal = dummyControl.getDummyThemeAttribute()
        self.assertIsNotNone(themeVal, "Broken theme property setter")

    def testBareException(self):

        logging = TestThemeProperty.classLogger
        dummyControl: DummyControl = DummyControl()
        dummyControl.setDummyThemeAttribute(42.0)

        themeVal = dummyControl.getDummyThemeAttribute()
        logging.info(f"themeVal: {themeVal}")

        themeVal = dummyControl._dummyThemeAttribute = 52

        self.assertEqual(themeVal, 52, "Change to underlying value is broken")

if __name__ == '__main__':
    unittest.main(exit=False)
