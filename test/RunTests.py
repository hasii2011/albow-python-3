
import unittest
from unittest import TestSuite
from unittest import TestLoader

from TestReferences import TestReferences
from TestScheduledCall import TestScheduledCall
from TestScheduler import TestScheduler
from TestThemeConfiguration import TestThemeConfiguration
from TestThemeProperty import TestThemeProperty

# Initialize the test suite
testLoader: TestLoader = unittest.TestLoader()
suite: TestSuite = unittest.TestSuite()


suite.addTest(testLoader.loadTestsFromTestCase(TestScheduler))
suite.addTest(testLoader.loadTestsFromTestCase(TestReferences))
suite.addTest(testLoader.loadTestsFromTestCase(TestScheduledCall))
suite.addTest(testLoader.loadTestsFromTestCase(TestThemeConfiguration))
suite.addTest(testLoader.loadTestsFromTestCase(TestThemeProperty))


# initialize a runner, pass it your suite and run it
runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)

print(result)