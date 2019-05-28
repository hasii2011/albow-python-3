
from pkg_resources import resource_filename

import logging

from pygame.font import Font

from albow.themes.ThemeError import ThemeError

"""
A Theme instance constituting the root of the theme hierarchy. It holds other Theme objects corresponding 
to particular classes, and default values for any theme attributes not specified by the class-specific 
themes. See Theme Lookup for an example of a partial theme hierarchy.

Applications can modify the contents of the theme hierarchy, or replace it altogether by assigning to theme.root.
"""


class Theme:
    """
    Instances of the Theme class are used to construct the theme hierarchy in which the values of theme
    properties are looked up. See Theme Lookup for details of how the theme hierarchy is structured and
    how the lookup process works.

    Theme Lookup
    ------------
    Values for theme properties are looked up in a hierarchy of Theme objects, beginning with
    themeRoot.
    The root Theme object contains two kinds of attributes: default values for theme properties, and other
    Theme objects containing values pertaining to specific classes.

    A value for a particular class *C* is looked up as follows. First, theme.themeRoot is looked in for a Theme object
    for class *C*, and that Theme object is looked in for a value for the attribute in question. If a value is found,
    it is returned. Otherwise, the process is repeated for each of *C*'s base classes, in method resolution order. If a
    value is still not found for the attribute, theme.root itself is looked in for a default value. (If it's not
    there either, an AttributeError results.)

    As a further refinement, a Theme object can be based on another Theme object. When looking in a Theme object
    for an attribute, if not found it will be looked for in the base theme, if any, and so forth.

    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    DARK_GRAY = (64, 64, 64)
    GRAY = (128, 128, 128)
    LIGHT_GRAY = (212, 208, 200)
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    LAMAS_BLACK = (42, 41, 41)
    LAMAS_GREY = (208, 210, 211)
    LAMAS_LIGHT_BLUE = (24, 189, 207)
    LAMAS_MEDIUM_BLUE = (106, 148, 204)
    LAMAS_DARK_BLUE = (65, 108, 178)
    LAMAS_OFF_WHITE = (255, 255, 244)

    BUILT_IN_FONT = "Vera.ttf"
    BUILT_IN_BOLD_FONT = "VeraBd.ttf"

    DEFAULT_PKG = "albow.themes.resources"

    ourThemeRoot = None

    fontCache = {}
    """
    Keep the theme fonts in their own cache separate from API consumer fonts
    """

    def __init__(self, name, base=None):
        """

        Args:
            name:  The name of the theme

            base: A Theme object can be based on another Theme object. When looking in a Theme object
                for an attribute, if not found it will be looked for in the base theme
        """
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.base = base

    def get(self, cls, name):
        try:
            return self.lookup(cls, name)
        except ThemeError:
            raise AttributeError("No value found in theme %s for '%s' of %s.%s" %
                                 (self.name, name, cls.__module__, cls.__name__))

    def lookup(self, cls, name):

        self.logger.debug("Theme(%s),lookup(%s, %s)", self.name, cls, name)
        for base_class in cls.__mro__:
            class_theme = getattr(self, base_class.__name__, None)
            if class_theme:
                try:
                    return class_theme.lookup(cls, name)
                except ThemeError:
                    pass
        else:
            try:
                return getattr(self, name)
            except AttributeError:
                base_theme = self.base
                if base_theme:
                    return base_theme.lookup(cls, name)
                else:
                    raise ThemeError

    def get_font(self, cls, name):

        self.logger.debug(f"Theme.get_font({cls}, {name})")
        spec = self.get(cls, name)
        if spec:

            self.logger.debug(f"font spec = {spec}")

            fontPath = self._findFontFile(spec)
            font = self._loadFont(fontPath=fontPath, fontSize=spec[0])
            return font

    def add_theme(self, name):
        setattr(self, name, Theme(name))

    def _findFontFile(self, spec: tuple):

        fontName = spec[1]
        fileName = resource_filename(Theme.DEFAULT_PKG, fontName)
        return fileName

    def _loadFont(self, fontPath: str, fontSize: int) -> Font:

        key = (fontPath, fontSize)
        font = Theme.fontCache.get(key)
        if font is None:
            try:
                font = Font(fontPath, fontSize)
            except IOError as e:
                raise e.__class__(f"{e}: {fontPath}")

        Theme.fontCache[key] = font
        return font

    def __str__(self):
        return self.name

    @classmethod
    def getThemeRoot(cls):
        return Theme.ourThemeRoot

    @classmethod
    def setThemeRoot(cls, theThemeRoot: "Theme"):

        Theme.ourThemeRoot = theThemeRoot
