
import os

from os import sep as osSep
from os import path as osPath
from os import getcwd
from os import chdir

from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain
from unittest import expectedFailure

from test.TestBase import TestBase

from albow.core.ResourceUtility import ResourceUtility

UNIT_TEST_DIR_NAME:       str = 'test'
RESOURCE_DIR_NAME:        str = 'testresources'
TEST_SOUND_RELATIVE_PATH: str = f'{RESOURCE_DIR_NAME}{osSep}TestSound.mp3'


class TestResourceUtility(TestBase):

    ourLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""
        TestResourceUtility.ourLogger = getLogger(__name__)
        self.logger = TestResourceUtility.ourLogger

    @expectedFailure
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

        self._findTestResourceDirectory()

        dummySound = ResourceUtility.load_sound(TEST_SOUND_RELATIVE_PATH)
        self.logger.info(f"{dummySound}")

    def testLoadSoundFail(self):

        self._findTestResourceDirectory()

        ResourceUtility.sound_cache = None
        dummySound = ResourceUtility.load_sound(TEST_SOUND_RELATIVE_PATH)

        self.assertEqual(first=ResourceUtility.dummy_sound, second=dummySound, msg="Did not get the dummy sound")

    @expectedFailure
    def testGetImageFail(self):

        ResourceUtility.get_image("")

    def _findTestResourceDirectory(self):

        self.logger.info(f'current directory: {getcwd()}')
        if osPath.isdir(f'{UNIT_TEST_DIR_NAME}{osSep}{RESOURCE_DIR_NAME}'):
            chdir(f'{UNIT_TEST_DIR_NAME}')
        if osPath.isdir(RESOURCE_DIR_NAME):
            return
        else:
            chdir("../")
            return self._findTestResourceDirectory()


if __name__ == '__main__':
    unitTestMain()
