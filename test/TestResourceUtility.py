
import os

from logging import Logger
from logging import getLogger

from unittest import main as unitTestMain
from unittest import expectedFailure

from pkg_resources import resource_filename

from test.TestBase import TestBase

from albow.core.ResourceUtility import ResourceUtility

UNIT_TEST_DIR_NAME:       str = 'test'
RESOURCE_DIR_NAME:        str = 'testresources'
TEST_SOUND_RELATIVE_PATH: str = f'TestSound.mp3'


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

        fqFileName: str = self.getFullResourcePath(TEST_SOUND_RELATIVE_PATH)

        dummySound = ResourceUtility.load_sound(fqFileName)
        self.logger.info(f"{dummySound}")

    def testLoadSoundFail(self):

        fqFileName: str = self.getFullResourcePath(TEST_SOUND_RELATIVE_PATH)

        ResourceUtility.sound_cache = None
        dummySound = ResourceUtility.load_sound(fqFileName)

        self.assertEqual(first=ResourceUtility.dummy_sound, second=dummySound, msg="Did not get the dummy sound")

    @expectedFailure
    def testGetImageFail(self):

        ResourceUtility.get_image("")

    def getFullResourcePath(self, filename: str) -> str:

        fqFileName: str = resource_filename(TestBase.RESOURCES_PACKAGE_NAME, filename)

        return fqFileName


if __name__ == '__main__':
    unitTestMain()
