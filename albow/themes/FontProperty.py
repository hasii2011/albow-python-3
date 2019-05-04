
from albow.themes.Theme import themeRoot

from albow.themes.ThemeProperty import ThemeProperty



class FontProperty(ThemeProperty):

    def get_from_theme(self, cls, name):
        return themeRoot.get_font(cls, name)
