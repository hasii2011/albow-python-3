
import logging

from albow.core.ResourceUtility import ResourceUtility

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
            return ResourceUtility.get_font(*spec)

    def add_theme(self, name):
        setattr(self, name, Theme(name))

    @staticmethod
    def initializeDefaultTheme():

        global themeRoot
        print("")


themeRoot = Theme('root')
themeRoot.font = (15, "Vera.ttf")
themeRoot.fg_color = (0, 0, 0)
themeRoot.bg_color = None
themeRoot.bg_image = None
themeRoot.scale_bg = False
themeRoot.border_width = 0
themeRoot.border_color = None
themeRoot.margin = 0
themeRoot.tab_bg_color = None
# root.sel_color = (63, 165, 254)
themeRoot.sel_color = (208, 210, 211)
themeRoot.highlight_color = None
themeRoot.disabled_color = None
themeRoot.highlight_bg_color = None
themeRoot.enabled_bg_color = None
themeRoot.disabled_bg_color = None

themeRoot.RootWidget = Theme('RootWidget')
themeRoot.RootWidget.bg_color = (0, 0, 0)

themeRoot.Label = Theme("Label")
themeRoot.Label.bg_color = (65, 108, 178)
themeRoot.Label.fg_color = Theme.WHITE

themeRoot.Button = Theme('Button')
themeRoot.Button.margin = 8
themeRoot.Button.border_width = 2
themeRoot.Button.font = (18, "VeraBd.ttf")
themeRoot.Button.fg_color = Theme.WHITE
themeRoot.Button.highlight_color = (0, 0, 0) # fg
# root.Button.disabled_color = (64, 64, 64) # fg
themeRoot.Button.disabled_color = (23, 62, 67) # fg  17 3e 43

themeRoot.Button.highlight_bg_color = (255, 165, 78)

themeRoot.Button.enabled_bg_color = (65, 108, 178)
themeRoot.Button.disabled_bg_color = (106, 148, 204)

themeRoot.ImageButton = Theme('ImageButton')
themeRoot.ImageButton.highlight_color = (0, 128, 255)

themeRoot.CheckWidget = Theme('CheckWidget')
themeRoot.CheckWidget.smooth = False

themeRoot.framed = Theme('framed')
themeRoot.framed.border_width = 1
themeRoot.framed.margin = 3

themeRoot.Field = Theme('Field', base=themeRoot.framed)

themeRoot.Dialog = Theme('Dialog')
themeRoot.Dialog.bg_color = (224, 224, 224)
themeRoot.Dialog.border_width = 2
themeRoot.Dialog.margin = 15

themeRoot.DirPathView = Theme('DirPathView', base=themeRoot.framed)

themeRoot.FileListView = Theme('FileListView', base=themeRoot.framed)
themeRoot.FileListView.scroll_button_color = (64, 64, 64)

themeRoot.FileDialog = Theme("FileDialog")
themeRoot.FileDialog.up_button_text = "<--"


themeRoot.PaletteView = Theme('PaletteView')
themeRoot.PaletteView.sel_width = 2
themeRoot.PaletteView.scroll_button_size = 16
themeRoot.PaletteView.scroll_button_color = (64, 64, 64)
themeRoot.PaletteView.highlight_style = 'reverse'

themeRoot.TableView = Theme("TableView")
themeRoot.TableView.bg_color = (65, 108, 178)

themeRoot.TextScreen = Theme('TextScreen')
themeRoot.TextScreen.heading_font = (24, "VeraBd.ttf")
themeRoot.TextScreen.button_font = (18, "VeraBd.ttf")
themeRoot.TextScreen.margin = 20

themeRoot.TabPanel = Theme('TabPanel')
themeRoot.TabPanel.tab_font = (18, "Vera.ttf")
themeRoot.TabPanel.tab_height = 24
themeRoot.TabPanel.tab_border_width = 0
themeRoot.TabPanel.tab_spacing = 4
themeRoot.TabPanel.tab_margin = 0
#
# There is a bug here;  These colors are not being properly applied
#
themeRoot.TabPanel.tab_fg_color = (24, 189, 207)
themeRoot.TabPanel.default_tab_bg_color = (106, 148, 204)
themeRoot.TabPanel.tab_area_bg_color = (208, 210, 211)

themeRoot.TabPanel.tab_dimming = 0.75
# root.TabPanel.use_page_bg_color_for_tabs = True

themeRoot.CheckWidget.smooth = True

themeRoot.MultiChoice = Theme("MultiChoice")
themeRoot.MultiChoice.sel_width = 1
themeRoot.MultiChoice.highlight_color = themeRoot.sel_color
themeRoot.MultiChoice.margin = 8
themeRoot.MultiChoice.cell_margin = 2

themeRoot.TextMultiChoice = Theme("TextMultiChoice")
themeRoot.TextMultiChoice.sel_color = None
themeRoot.TextMultiChoice.highlight_style = 'arrows'

themeRoot.ImageMultiChoice = Theme("ImageMultiChoice")
themeRoot.ImageMultiChoice.sel_color = (192, 192, 192)
themeRoot.ImageMultiChoice.highlight_style = 'fill'

themeRoot.menu = Theme('menu')
themeRoot.menu.bg_color = (255, 255, 255)
themeRoot.menu.fg_color = (0, 0, 0)
themeRoot.menu.disabled_color = (128, 128, 128)
themeRoot.menu.margin = 8

themeRoot.MenuBar = Theme('MenuBar', base=themeRoot.menu)
themeRoot.MenuBar.border_width = 0

themeRoot.Menu = Theme('Menu', base=themeRoot.menu)
themeRoot.Menu.border_width = 1

themeRoot.MusicVolumeControl = Theme('MusicVolumeControl', base=themeRoot.framed)
themeRoot.MusicVolumeControl.fg_color = (0x40, 0x40, 0x40)
