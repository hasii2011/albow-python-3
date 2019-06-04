
import os

import logging

from logging import Logger

import pygame

from test.TestBase import TestBase

from albow.themes.Theme import Theme

THEMES_RESOURCES_PACKAGE = "albow.themes.resources"
BUILT_IN_BOLD_FONT_NAME = "VeraBd.ttf"


class TestTheme(TestBase):

    ourLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()
        TestTheme.ourLogger = logging.getLogger(__name__)

    def setUp(self):
        """"""
        self.logger = TestTheme.ourLogger

    def tearDown(self):

        Theme.fontCache = {}

    def testFontLoad(self):

        testTheme: Theme = Theme(name="bogus")
        fontSpec: tuple = (18, BUILT_IN_BOLD_FONT_NAME)
        fontPath: str = testTheme._findFontFile(fontSpec)

        exists = os.path.isfile(fontPath)
        self.assertTrue(exists, "Where is my font!")

    def testFontCacheLoad(self):

        self.assertTrue(len(Theme.fontCache) == 0, "Oops not in an initial state")

        pygame.init()

        testTheme: Theme = Theme(name="bogus")

        fontSpec: tuple = (18, BUILT_IN_BOLD_FONT_NAME)
        fontPath: str = testTheme._findFontFile(fontSpec)
        testTheme._loadFont(fontPath=fontPath, fontSize=fontSpec[0])

        self.assertTrue(len(Theme.fontCache) == 1, "Oops cache is not working")

    def testFontCacheHit(self):
        pygame.init()

        testTheme: Theme = Theme(name="bogus")

        fontSpec: tuple = (18, BUILT_IN_BOLD_FONT_NAME)
        fontPath: str = testTheme._findFontFile(fontSpec)
        font1 = testTheme._loadFont(fontPath=fontPath, fontSize=fontSpec[0])
        font2 = testTheme._loadFont(fontPath=fontPath, fontSize=fontSpec[0])

        self.assertEqual(first=font1, second=font2, msg="Should be the one from the cache")
