
import logging
import time

from logging import Logger

import unittest

from TestBase import TestBase

from albow.core.Scheduler import Scheduler


class TestScheduler(TestBase):
    """
    A test class
    """
    ourLogger: Logger = None
    """
    A class logger
    """

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""
        TestScheduler.ourLogger = logging.getLogger(__name__)

    def tearDown(self):
        #
        # Clean up
        #
        Scheduler.ourScheduledCalls.clear()

    def testSingletonBehavior(self):

        TestScheduler.ourLogger.info("Testing singleton behavior")
        self.assertTrue(len(Scheduler.ourScheduledCalls) == 0, msg="There should be no scheduled calls at start up")

    def testBasicScheduling(self):

        TestScheduler.ourLogger.info("Test basic scheduling")

        retToken = Scheduler.schedule_call(delay=5000, func=TestScheduler.callbackFunction, repeat=False)

        self.assertIsNotNone(retToken, "I did not get my token")
        nScheduledItems = len(Scheduler.ourScheduledCalls)

        self.assertTrue(nScheduledItems == 1, "Too many scheduled calls")

    def testCancelCall(self):

        TestScheduler.ourLogger.info("Test cancel Call")

        retToken = Scheduler.schedule_call(delay=5000, func=TestScheduler.callbackFunction, repeat=False)

        Scheduler.cancel_call(retToken)

        nScheduledItems = len(Scheduler.ourScheduledCalls)

        self.assertTrue(nScheduledItems == 0, "Failed to remove a scheduled calls")

    def testMakeDueCalls(self):

        TestScheduler.ourLogger.info("Test make due calls")

        retToken = Scheduler.schedule_call(delay=5000, func=TestScheduler.callbackFunction, repeat=False)

        timeNow = Scheduler.timestamp()
        untilTime = timeNow + 10000

        time.sleep(6.0)

        Scheduler.make_due_calls(time_now=timeNow, until_time=untilTime)


    @staticmethod
    def callbackFunction():

        TestScheduler.ourLogger.info("I have been called")


if __name__ == '__main__':
    unittest.main()
