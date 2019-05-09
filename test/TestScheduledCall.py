
import logging
from logging import Logger

import unittest

from TestBase import TestBase

from albow.core.ScheduledCall import ScheduledCall
from albow.core.Scheduler import Scheduler


class TestSchedulerCall(TestBase):
    """
    """
    classLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""
        TestSchedulerCall.classLogger = logging.getLogger(__name__)

    def testEquality(self):

        whenToExecute = Scheduler.timestamp()

        TestSchedulerCall.classLogger.info("whenToExecute: %s", whenToExecute)

        sc1: ScheduledCall = ScheduledCall(timeToExecute=whenToExecute, func=TestSchedulerCall.callback1, interval=0)
        sc2: ScheduledCall = ScheduledCall(timeToExecute=whenToExecute, func=TestSchedulerCall.callback1, interval=0)

        self.assertEqual(first=sc1, second=sc2, msg="Unit test equality is failing")

        self.assertTrue((sc1 == sc2), msg="Basic equality is failing")

    def testNonEqualityWithTime(self):

        whenToExecute1 = Scheduler.timestamp()
        whenToExecute2 = Scheduler.timestamp()

        TestSchedulerCall.classLogger.info("whenToExecute1: %s, whenToExecute2: %s", whenToExecute1, whenToExecute2)

        sc1: ScheduledCall = ScheduledCall(timeToExecute=whenToExecute1, func=TestSchedulerCall.callback1, interval=0)
        sc2: ScheduledCall = ScheduledCall(timeToExecute=whenToExecute2, func=TestSchedulerCall.callback1, interval=0)

        ans: bool = sc1 == sc2

        self.assertFalse(ans, "time inequality is failing")

    def testNonEqualityWithCallback(self):

        whenToExecute = Scheduler.timestamp()

        sc1: ScheduledCall = ScheduledCall(timeToExecute=whenToExecute, func=TestSchedulerCall.callback1, interval=0)
        sc2: ScheduledCall = ScheduledCall(timeToExecute=whenToExecute, func=TestSchedulerCall.callback2, interval=0)

        ans: bool = sc1 == sc2

        self.assertFalse(ans, "time inequality is failing")

    def testNonEqualityWithInterval(self):

        whenToExecute = Scheduler.timestamp()

        sc1: ScheduledCall = ScheduledCall(timeToExecute=whenToExecute, func=TestSchedulerCall.callback1, interval=40)
        sc2: ScheduledCall = ScheduledCall(timeToExecute=whenToExecute, func=TestSchedulerCall.callback2, interval=50)

        ans: bool = (sc1 == sc2)

        self.assertFalse(ans, "Interval inequality is failing")

    def testStringRepresentation(self):

        whenToExecute = Scheduler.timestamp()

        sc: ScheduledCall = ScheduledCall(timeToExecute=whenToExecute, func=TestSchedulerCall.callback1, interval=40)

        strRep = sc.__str__()
        self.assertIsNotNone(strRep, "Class string rep did not return anything")

        TestSchedulerCall.classLogger.info("String representation: %s", sc)

    @staticmethod
    def callback1():

        TestSchedulerCall.classLogger.info("callbackFunction1 has executed")

    @staticmethod
    def callback2():

        TestSchedulerCall.classLogger.info("callbackFunction2 has executed")


if __name__ == '__main__':
    unittest.main()
