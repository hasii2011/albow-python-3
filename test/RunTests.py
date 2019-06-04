
import unittest
from unittest import TestSuite
from unittest import TestLoader

from test.TestFindResources import TestFindResources
from test.TestPredictor import TestPredictor
from test.TestReferences import TestReferences
from test.TestResourceUtility import TestResourceUtility
from test.TestScheduledCall import TestScheduledCall
from test.TestTheme import TestTheme
from test.TestThemeProperty import TestThemeProperty

from test.TestScheduler import TestScheduler


def main():
    # Initialize the test suite
    testLoader: TestLoader = unittest.TestLoader()
    suite: TestSuite = unittest.TestSuite()

    suite.addTest(testLoader.loadTestsFromTestCase(TestFindResources))
    suite.addTest(testLoader.loadTestsFromTestCase(TestPredictor))
    suite.addTest(testLoader.loadTestsFromTestCase(TestReferences))
    suite.addTest(testLoader.loadTestsFromTestCase(TestResourceUtility))
    suite.addTest(testLoader.loadTestsFromTestCase(TestScheduledCall))
    suite.addTest(testLoader.loadTestsFromTestCase(TestTheme))
    suite.addTest(testLoader.loadTestsFromTestCase(TestThemeProperty))

    suite.addTest(testLoader.loadTestsFromTestCase(TestScheduler))

    # initialize a runner, pass it our suite and run it
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    print(result)


if __name__ == '__main__':
    main()
