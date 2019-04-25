
from albow.themes.Theme import root

from albow.themes.ThemeProperty import ThemeProperty



class FontProperty(ThemeProperty):

    def get_from_theme(self, cls, name):
        return root.get_font(cls, name)
