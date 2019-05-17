
import unittest

import logging
from logging import Logger

import random

import configparser

from TestBase import TestBase

from albow.themes.Theme import Theme
from albow.themes.ThemeLoader import ThemeLoader

CURRENTLY_KNOWN_THEMES = [
    "RootWidget",
    "Label",
    "Button",
    "ImageButton",
    "CheckWidget",
    "FrameBase",
    "Field",
    "Dialog",
    "DirPathView",
    "FileListView",
    "FileDialog",
    "PaletteView",
    "TableView",
    "TextScreen",
    "TabPanel",
    "MultiChoice",
    "TextMultiChoice",
    "ImageMultiChoice",
    "MenuBase",
    "Menu",
    "MusicVolumeControl"
]
NUMBER_OF_THEMES_TO_CHECK = 5


class TestThemeConfiguration(TestBase):

    classLogger: Logger = None

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()

    def setUp(self):
        """"""
        TestThemeConfiguration.classLogger = logging.getLogger(__name__)

    def tearDown(self):
        """
        cleanup
        """

    def testConfigWrite(self):
        """
        Just wrote this test so I don't have manually create the _.ini_ configuration file
        """

        logger = TestThemeConfiguration.classLogger

        themeRoot = Theme.getThemeRoot()

        self.assertIsNone(themeRoot)

        Theme.initializeDefaultTheme()

        themeRoot = Theme.getThemeRoot()

        self.assertIsNotNone(themeRoot, "WTH, the themeRoot is empty")

        varDict = vars(themeRoot)

        sectionName = varDict['name']
        logger.info("sectionName: %s", sectionName)
        config = configparser.ConfigParser()
        config[sectionName] = {}
        section = config[sectionName]

        self.updateConfigSection(varDict, logger, section, config)

        with open('theme.ini', 'w') as configfile:
            config.write(configfile)

    def testFindThemeConfig(self):

        logger = TestThemeConfiguration.classLogger

        themeLoader: ThemeLoader = ThemeLoader()
        workingDir: str = themeLoader.findConfigFile()

        self.assertIsNotNone(workingDir, "Failure did not find the file")

    @unittest.skip("I don't like to see stack traces, even on passes")
    # @unittest.expectedFailure
    def testFailToFindThemeConfig(self):

        themeLoader: ThemeLoader = ThemeLoader(themeFilename="BogusFile.txt")
        themeLoader.findConfigFile()

    def testLoadThemeSuccess(self):

        logger = TestThemeConfiguration.classLogger

        themeLoader: ThemeLoader = ThemeLoader()
        try:
            themeLoader.findConfigFile()
            themeLoader.load()

            self.assertIsNotNone(themeLoader.themeRoot, "Uh Oh, a theme is not loaded")

            #
            # Test a few random ones
            #
            for x in range(NUMBER_OF_THEMES_TO_CHECK):
                name = random.choice(CURRENTLY_KNOWN_THEMES)
                logger.info(f"Checking {name}")
                self.assertTrue(hasattr(themeLoader.themeRoot, name), "Missing a them")

        except FileNotFoundError:
            self.assertTrue(False, "We should be able to find default file")

    def updateConfigSection(self, varDict, logger, section, config):

        for attr in varDict:
            if "logger" in attr:
                logger.debug("Ignoring: %s", attr)
            elif attr[0].isupper():
                logger.debug("Theme class name: %s", attr)
                config[attr] = {}
                anotherSection = config[attr]
                embeddedObj = varDict[attr]
                embeddedDict = vars(embeddedObj)
                logger.debug("embeddedDict: %s", embeddedDict)
                self.updateConfigSection(embeddedDict, logger, anotherSection, config)
            else:
                attrValue = varDict[attr]
                logger.debug("Attr: %s, value: %s", attr, attrValue)
                if attrValue is None:
                    section[attr] = ''
                else:
                    section[attr] = str(attrValue)
        return section


if __name__ == '__main__':
    print(__name__)
    unittest.main(exit=False)
