
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

    weHaveBeenCalledToken: bool = False

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""
        TestScheduler.ourLogger = logging.getLogger(__name__)
        # Scheduler.ourLogger.setLevel(logging.DEBUG)

    def tearDown(self):
        #
        # Clean up
        #
        Scheduler.ourScheduledCalls.clear()
        TestScheduler.weHaveBeenCalledToken = False

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

        TestScheduler.ourLogger.info("Test Scheduler make call that are due")

        retToken = Scheduler.schedule_call(delay=0, func=TestScheduler.callbackFunction, repeat=False)

        TestScheduler.ourLogger.info("Task %s scheduled", retToken)

        TestScheduler.ourLogger.info("Sleepy time ...")
        time.sleep(10.0)

        TestScheduler.ourLogger.info("We've awakened . . . ")

        timeNow = Scheduler.timestamp()
        untilTime = timeNow + 5000
        aTime = Scheduler.make_due_calls(time_now=timeNow, until_time=untilTime)
        TestScheduler.ourLogger.info("aTime: %s", aTime)

        self.assertTrue(TestScheduler.weHaveBeenCalledToken, "The token should have been set, but was not")

    def testMakeDueCallNothingScheduled(self):

        timeNow = Scheduler.timestamp()
        untilTime = timeNow + 5000
        aTime = Scheduler.make_due_calls(time_now=timeNow, until_time=untilTime)
        TestScheduler.ourLogger.info("aTime: %s", aTime)

        self.assertFalse(TestScheduler.weHaveBeenCalledToken, "Someone set the token and should not have")

    def testMakeScheduledCalls(self):

        TestScheduler.ourLogger.info("Test legacy make_scheduled_calls")

        retToken = Scheduler.schedule_call(delay=0, func=TestScheduler.callbackFunction, repeat=False)

        TestScheduler.ourLogger.info("Task %s scheduled", retToken)

        TestScheduler.ourLogger.info("Sleepy time ...")
        time.sleep(5.0)

        Scheduler.make_scheduled_calls()
        self.assertTrue(TestScheduler.weHaveBeenCalledToken, "The token should have been set, but was not")

    @staticmethod
    def callbackFunction():

        TestScheduler.ourLogger.info("I have been called: '%s'", TestScheduler.callbackFunction.__name__)
        TestScheduler.weHaveBeenCalledToken = True

if __name__ == '__main__':
    unittest.main()
