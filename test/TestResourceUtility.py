
import os

import logging
from logging import Logger

import unittest

from test.TestBase import TestBase

from albow.core.ResourceUtility import ResourceUtility

TEST_SOUND_RELATIVE_PATH = "testresources/TestSound.mp3"


class TestResourceUtility(TestBase):

    ourLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""
        TestResourceUtility.ourLogger = logging.getLogger(__name__)
        self.logger = TestResourceUtility.ourLogger

    @unittest.expectedFailure
    def testFindResourceDirFailure(self):
        ResourceUtility.find_resource_dir()

    def testFindResourceDirSuccess(self):

        currentDirectory = os.getcwd()
        self.logger.info(f"cwd: '{currentDirectory}'")

        newDir = "resources"
        os.mkdir(newDir)
        resourceDir = ResourceUtility.find_resource_dir()

        self.assertIsNotNone(resourceDir, "Failed to return something")

        self.assertEqual(resourceDir.lower(), f"{currentDirectory}/resources".lower(), "Found in wrong place")
        os.rmdir("resources")

    def testLoadSound(self):

        import pygame
        pygame.init()

        dummySound = ResourceUtility.load_sound("%s" % TEST_SOUND_RELATIVE_PATH)
        self.logger.info(f"{dummySound}")

    def testLoadSoundFail(self):

        ResourceUtility.sound_cache = None
        dummySound = ResourceUtility.load_sound(TEST_SOUND_RELATIVE_PATH)

        self.assertEqual(first=ResourceUtility.dummy_sound, second=dummySound, msg="Did not get the dummy sound")

    @unittest.expectedFailure
    def testGetImageFail(self):

        ResourceUtility.get_image("")


if __name__ == '__main__':
    unittest.main()
