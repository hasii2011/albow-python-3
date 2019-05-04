
import logging

import albow

from albow.themes.ThemeError import ThemeError

class Theme:

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BUILT_IN_FONT = "VeraBd.ttf"

    def __init__(self, name, base = None):
        """

        :param name:    Name of theme, for debugging
        :param base:    Theme or None   Theme on which this theme is based
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

        self.logger.debug("Theme.get_font(%s, %s)", cls, name)
        spec = self.get(cls, name)
        if spec:

            self.logger.debug("font spec = %s", spec)
            return albow.Res.get_font(*spec)

    def add_theme(self, name):
        setattr(self, name, Theme(name))

root = Theme('root')
root.font = (15, "Vera.ttf")
root.fg_color = (0, 0, 0)
root.bg_color = None
root.bg_image = None
root.scale_bg = False
root.border_width = 0
root.border_color = None
root.margin = 0
root.tab_bg_color = None
# root.sel_color = (63, 165, 254)
root.sel_color = (208, 210, 211)
root.highlight_color = None
root.disabled_color = None
root.highlight_bg_color = None
root.enabled_bg_color = None
root.disabled_bg_color = None

root.RootWidget = Theme('RootWidget')
root.RootWidget.bg_color = (0, 0, 0)

root.Label = Theme("Label")
root.Label.bg_color = (65, 108, 178)
root.Label.fg_color = Theme.WHITE

root.Button = Theme('Button')
root.Button.margin = 8
root.Button.border_width = 2
root.Button.font = (18, "VeraBd.ttf")
root.Button.fg_color = Theme.WHITE
root.Button.highlight_color = (0, 0, 0) # fg
# root.Button.disabled_color = (64, 64, 64) # fg
root.Button.disabled_color = (23, 62, 67) # fg  17 3e 43

root.Button.highlight_bg_color = (255, 165, 78)

root.Button.enabled_bg_color = (65,108,178)
root.Button.disabled_bg_color = (106,148,204)

root.ImageButton = Theme('ImageButton')
root.ImageButton.highlight_color = (0, 128, 255)

root.CheckWidget = Theme('CheckWidget')
root.CheckWidget.smooth = False

framed = Theme('framed')
framed.border_width = 1
framed.margin = 3

root.Field = Theme('Field', base = framed)

root.Dialog = Theme('Dialog')
root.Dialog.bg_color = (224, 224, 224)
root.Dialog.border_width = 2
root.Dialog.margin = 15

root.DirPathView = Theme('DirPathView', base = framed)

root.FileListView = Theme('FileListView', base = framed)
root.FileListView.scroll_button_color = (64, 64, 64)

root.FileDialog = Theme("FileDialog")
root.FileDialog.up_button_text = "<--"


root.PaletteView = Theme('PaletteView')
root.PaletteView.sel_width = 2
root.PaletteView.scroll_button_size = 16
root.PaletteView.scroll_button_color = (64, 64, 64)
root.PaletteView.highlight_style = 'reverse'

root.TableView = Theme("TableView")
root.TableView.bg_color = (65, 108, 178)

root.TextScreen = Theme('TextScreen')
root.TextScreen.heading_font = (24, "VeraBd.ttf")
root.TextScreen.button_font = (18, "VeraBd.ttf")
root.TextScreen.margin = 20

root.TabPanel = Theme('TabPanel')
root.TabPanel.tab_font = (18, "Vera.ttf")
root.TabPanel.tab_height = 24
root.TabPanel.tab_border_width = 0
root.TabPanel.tab_spacing = 4
root.TabPanel.tab_margin = 0
#
# There is a bug here;  These colors are not being properly applied
#
root.TabPanel.tab_fg_color = (24, 189, 207)
root.TabPanel.default_tab_bg_color = (106, 148, 204)
root.TabPanel.tab_area_bg_color = (208, 210, 211)

root.TabPanel.tab_dimming = 0.75
#root.TabPanel.use_page_bg_color_for_tabs = True

root.CheckWidget.smooth = True

root.MultiChoice = Theme("MultiChoice")
root.MultiChoice.sel_width = 1
root.MultiChoice.highlight_color = root.sel_color
root.MultiChoice.margin = 8
root.MultiChoice.cell_margin = 2

root.TextMultiChoice = Theme("TextMultiChoice")
root.TextMultiChoice.sel_color = None
root.TextMultiChoice.highlight_style = 'arrows'

root.ImageMultiChoice = Theme("ImageMultiChoice")
root.ImageMultiChoice.sel_color = (192, 192, 192)
root.ImageMultiChoice.highlight_style = 'fill'

menu = Theme('menu')
menu.bg_color = (255, 255, 255)
menu.fg_color = (0, 0, 0)
menu.disabled_color = (128, 128, 128)
menu.margin = 8

root.MenuBar = Theme('MenuBar', base = menu)
root.MenuBar.border_width = 0

root.Menu = Theme('Menu', base = menu)
root.Menu.border_width = 1

root.MusicVolumeControl = Theme('MusicVolumeControl', base = framed)
root.MusicVolumeControl.fg_color = (0x40, 0x40, 0x40)
