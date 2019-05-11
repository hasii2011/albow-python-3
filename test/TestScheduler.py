
import logging
import time
from time import localtime
from time import strftime


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
    callTime1 = 0
    callTime2 = 0
    callTime3 = 0
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

    def testSchedulingOrder(self):

        #
        # Purposely schedule in wrong order; Scheduler should execute in correct order
        #
        retToken1 = Scheduler.schedule_call(delay=1000, func=TestScheduler.callbackFunction1, repeat=False)
        retToken2 = Scheduler.schedule_call(delay=9000, func=TestScheduler.callbackFunction3, repeat=False)
        retToken3 = Scheduler.schedule_call(delay=5000, func=TestScheduler.callbackFunction2, repeat=False)

        TestScheduler.ourLogger.info("Wait long enough so that all tasks will be called in one shot")
        time.sleep(10.0)

        Scheduler.make_scheduled_calls()
        self.assertTrue( (TestScheduler.callTime1 < TestScheduler.callTime2) and
                          TestScheduler.callTime2 < TestScheduler.callTime3,
                         "Scheduler called tasks out of order")

    @staticmethod
    def callbackFunction():

        TestScheduler.ourLogger.info("I have been called: '%s'", TestScheduler.callbackFunction.__name__)
        TestScheduler.weHaveBeenCalledToken = True

    @staticmethod
    def callbackFunction1():

        TestScheduler.callTime1 = Scheduler.timestamp()
        prettyTime = strftime("%H:%M:%S", localtime(TestScheduler.callTime1))
        TestScheduler.ourLogger.info("`%s' executed at: %s",
                                     TestScheduler.callbackFunction1.__name__,
                                     prettyTime)

    @staticmethod
    def callbackFunction2():

        TestScheduler.callTime2 = Scheduler.timestamp()
        prettyTime = strftime("%H:%M:%S", localtime(TestScheduler.callTime2))
        TestScheduler.ourLogger.info("`%s' executed at: %s",
                                     TestScheduler.callbackFunction2.__name__,
                                     prettyTime)

    @staticmethod
    def callbackFunction3():

        TestScheduler.callTime3 = Scheduler.timestamp()
        prettyTime = strftime("%H:%M:%S", localtime(TestScheduler.callTime3))
        TestScheduler.ourLogger.info("`%s' executed at: %s",
                                     TestScheduler.callbackFunction3.__name__,
                                     prettyTime)


if __name__ == '__main__':
    unittest.main()
