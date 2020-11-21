
from logging import Logger
from logging import getLogger

from os import sep as osSep

from configparser import ConfigParser
from configparser import SectionProxy

from ast import literal_eval as make_tuple

from albow.themes.Theme import Theme


class ThemeLoader:

    DEFAULT_THEME_FILENAME: str = "default-theme.ini"

    DEFAULT_PKG:      str = "resources"
    ROOT_THEME_NAME:  str = "root"

    def __init__(self, themePkg: str = DEFAULT_PKG, themeFilename: str = DEFAULT_THEME_FILENAME):
        """
        """
        self.logger: Logger = getLogger(__name__)

        self.themePkg:      str = themePkg
        self.themeFilename: str = themeFilename

        self.topLevelClassThemes = []
        self.themeRoot = None

    def load(self):

        config = ConfigParser()

        import pkgutil

        bThemeData = pkgutil.get_data(__name__, f"{self.themePkg}{osSep}{self.themeFilename}")
        themeData = bThemeData.decode('ascii')

        self.logger.debug(f"{themeData=}")

        config.read_string(themeData)

        self.themeRoot = self.loadAClass(config[ThemeLoader.ROOT_THEME_NAME])

        self.extractThemeInstances(config)
        self.augmentInstancesWithBase()

    def augmentInstancesWithBase(self):

        varDict: dict = vars(self.themeRoot)

        for attr in varDict:
            if attr[0].isupper():
                embeddedTheme: Theme = getattr(self.themeRoot, attr)
                baseName: str = getattr(embeddedTheme, "base")
                if baseName is not None:
                    self.logger.debug(f"embeddedTheme: '{embeddedTheme}'' has base: '{embeddedTheme}'")
                    baseTheme: Theme = getattr(self.themeRoot, baseName)
                    setattr(embeddedTheme, "base", baseTheme)
                    self.logger.debug(f"Theme {embeddedTheme} has new base {baseTheme}")

    def loadAClass(self, classDict: SectionProxy) -> Theme:

        themeName = classDict["name"]

        theme = Theme(name=themeName)

        for attr in classDict:
            if self.ignoreAttribute(attr):
                pass
            else:
                attrStrValue: str = classDict[attr]
                if not attrStrValue:
                    setattr(theme, attr, None)
                elif "color" in attr or "font" in attr:
                    attrTuple = make_tuple(attrStrValue)
                    setattr(theme, attr, attrTuple)
                elif "True" in attrStrValue or "False" in attrStrValue:
                    attrBool = bool(attrStrValue)
                    setattr(theme, attr, attrBool)
                elif attrStrValue.isnumeric():
                    attrInt = int(attrStrValue)
                    setattr(theme, attr, attrInt)
                elif ThemeLoader.isFloat(attrStrValue):
                    floatAttr = float(attrStrValue)
                    setattr(theme, attr, floatAttr)
                else:
                    setattr(theme, attr, attrStrValue)

        return theme

    def extractThemeInstances(self, config: ConfigParser):
        """
        Creates theme instances for the various configuration sections
        Ignores the "root" theme.  Assumes it has been set

        Args:
            config:  The config parser

        Returns: Update `themeRoot`

        """
        sections = config.sections()
        assert self.themeRoot is not None, "Code change broke me"

        for idx in range(len(sections)):
            sectionName = sections[idx]
            if sectionName == ThemeLoader.ROOT_THEME_NAME:
                continue
            else:
                self.logger.debug("sectionName: '%s'", sectionName)
                classDict = config[sectionName]
                theme = self.loadAClass(classDict)
                #
                # Section name matches the attribute name on the
                # theme root
                #
                setattr(self.themeRoot, sectionName, theme)

    def ignoreAttribute(self, theAttr: str) -> bool:
        """
        We'll never restore the logger; The base attribute is handled specially; We handle embedded
        themes in a separate loop

        Args:
            theAttr: The attribute name to inspect

        Returns: True when the attribute is the logger, an embedded theme, or the attribute "base"

        """
        ans: bool = False

        if "logger" in theAttr or theAttr[0].isupper():
            self.logger.debug("Ignoring: %s", theAttr)
            ans = True

        return ans

    @staticmethod
    def isFloat(strValue: str):
        try:
            float(strValue)
        except ValueError:
            return False
        else:
            return True
