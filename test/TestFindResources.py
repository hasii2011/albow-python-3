
import logging

import unittest

from test.TestBase import TestBase

from pkg_resources import resource_filename
from pkg_resources import resource_exists

BUILT_IN_BOLD_FONT_NAME = "VeraBd.ttf"
BUILT_IN_FONT_NAME = "Vera.ttf"
DEFAULT_THEME_FILENAME = "default-theme.ini"
THEMES_RESOURCES_PACKAGE = "albow.themes.resources"


class TestFindResources(TestBase):

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""
        self.logger = logging.getLogger(__name__)

    def testFindDefaultTheme(self):

        self.assertTrue(resource_exists(THEMES_RESOURCES_PACKAGE, DEFAULT_THEME_FILENAME), "Missing theme file")
        fileName = resource_filename(THEMES_RESOURCES_PACKAGE, DEFAULT_THEME_FILENAME)

        self.assertIsNotNone(fileName)
        self.logger.info(f"fileName: `{fileName}`")

    def testFindBuiltInBaseFont(self):

        self.assertTrue(resource_exists(THEMES_RESOURCES_PACKAGE, "%s" % BUILT_IN_FONT_NAME), "Missing built-in font")
        fontFileName = resource_filename(THEMES_RESOURCES_PACKAGE, BUILT_IN_FONT_NAME)

        self.assertIsNotNone(fontFileName)
        self.logger.info(f"fontFileName: `{fontFileName}`")

    def testFindBuiltInBoldBaseFont(self):

        self.assertTrue(resource_exists(THEMES_RESOURCES_PACKAGE, BUILT_IN_BOLD_FONT_NAME), "Missing built-in bold font")

        boldFontFileName = resource_filename(THEMES_RESOURCES_PACKAGE, "%s" % BUILT_IN_BOLD_FONT_NAME)

        self.assertIsNotNone(boldFontFileName)
        self.logger.info(f"boldFontFileName: `{boldFontFileName}`")


if __name__ == '__main__':
    unittest.main()
