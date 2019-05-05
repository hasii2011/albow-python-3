
import sys

import logging

from albow.core.ResourceUtility import ResourceUtility
from albow.core.Screen import Screen
from albow.core.Shell import Shell

from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.layout.Column import Column
from albow.layout.Grid import Grid

from albow.themes.Theme import Theme

DEMO_TITLE_TEXT_SIZE = 24
DEMO_BUTTON_TEXT_SIZE = 14

class LaunchDemosScreen(Screen):
    """
    Buttons
    """

    def __init__(self, shell: Shell):
        """

        :param shell:
        """
        self.logger = logging.getLogger(__name__)
        #
        # Python 3 update
        #
        # Screen.__init__(self, shell)
        super().__init__(shell)

        self.shell     = shell
        f1             = ResourceUtility.get_font(DEMO_TITLE_TEXT_SIZE, Theme.BUILT_IN_FONT)
        titleAttrs = {
            'fg_color': Theme.BLACK,
            'bg_color': Theme.WHITE,
            'enabled_bg_color': Theme.WHITE,
            'highlight_color': (208,210,211),
            'highlighted': True,
            'align': 'c'
        }
        title = Label("Albow Demonstration", font=f1, **titleAttrs)
        emptyButtFont = ResourceUtility.get_font(DEMO_BUTTON_TEXT_SIZE, Theme.BUILT_IN_FONT)
        emptyButtAttrs = {
            'font': emptyButtFont
        }

        menuArray = [
            [
                self.screen_button("Text Screen",    shell.text_screen),
                self.screen_button("Text Fields",    shell.fields_screen),
                self.screen_button("Controls",       shell.controls_screen),
            ],
            [
                self.screen_button("Animation",    shell.anim_screen),
                self.screen_button("Grid View",    shell.grid_screen),
                self.screen_button("Palette View", shell.palette_screen),
            ],
            [
                self.screen_button("Image Array",   shell.image_array_screen),
                self.screen_button("Modal Dialogs", shell.dialog_screen),
                self.screen_button("Tab Panel",     shell.tab_panel_screen),
            ],
            [
                self.screen_button("Table View",  shell.table_screen),
                self.screen_button("MultiChoice", shell.multiChoiceScreen),
                self.screen_button("MenuBar",     shell.menuBarScreen)
            ],
            [
                self.screen_button("Music",   shell.musicScreen),
                self.screen_button("ListBox", shell.listBoxScreen),
                Button("Empty", **emptyButtAttrs)
            ]
        ]

        menuGrid = Grid(rows=menuArray, column_spacing=5, row_spacing=2)
        quitButton = Button("Quit", shell.quit)

        self.equallySizeButtons(menuArray)

        contents = Column([
            title,
            menuGrid,
            quitButton
        ], align='c', spacing=10)
        self.add_centered(contents)

    def screen_button(self, text: str, screen: Screen):

        buttFont = ResourceUtility.get_font(DEMO_BUTTON_TEXT_SIZE, Theme.BUILT_IN_FONT)
        buttAttrs = {
            'font': buttFont
        }
        retButton = Button(text, action=lambda: self.shell.show_screen(screen), **buttAttrs)
        return retButton

    def equallySizeButtons(self, menuArray):

        largestWidth: int = 0
        for buttRow in menuArray:
            for butt in buttRow:
                self.logger.debug("Button text: %s, width: %s", butt.text, butt.width)
                currWidth = butt.width
                if currWidth > largestWidth:
                    largestWidth = currWidth

        self.logger.debug("largestWidth: %s", largestWidth)

        for buttRow in menuArray:
            for butt in buttRow:
                butt.width = largestWidth

        return menuArray

    def quit(self):
        sys.exit(0)
