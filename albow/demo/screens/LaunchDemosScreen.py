
from typing import cast

import logging

from albow.core.ResourceUtility import ResourceUtility
from albow.core.ui.Screen import Screen
from albow.core.ui.Shell import Shell

from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.layout.Column import Column
from albow.layout.Grid import Grid

from albow.themes.Theme import Theme

DEMO_TITLE_TEXT_SIZE = 24
DEMO_BUTTON_TEXT_SIZE = 12


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

        from albow.demo.DemoShell import DemoShell
        self.shell = cast(DemoShell, shell)
        f1 = ResourceUtility.get_font(DEMO_TITLE_TEXT_SIZE, Theme.BUILT_IN_FONT)

        title = Label("Albow Demonstration", font=f1)
        #  emptyButton = Button("Empty", enabled=False)

        menuArray = [
            [
                self.screen_button("Text Screen", self.shell.text_screen),
                self.screen_button("Text Fields", self.shell.fields_screen),
                self.screen_button("Controls",    self.shell.controls_screen),
            ],
            [
                self.screen_button("Animation",    self.shell.anim_screen),
                self.screen_button("Grid View",    self.shell.grid_screen),
                self.screen_button("Palette View", self.shell.palette_screen),
            ],
            [
                self.screen_button("Image Array",   self.shell.image_array_screen),
                self.screen_button("Modal Dialogs", self.shell.dialog_screen),
                self.screen_button("Tab Panel",     self.shell.tab_panel_screen),
            ],
            [
                self.screen_button("Table View",  self.shell.table_screen),
                self.screen_button("MultiChoice", self.shell.multiChoiceScreen),
                self.screen_button("MenuBar",     self.shell.menuBarScreen)
            ],
            [
                self.screen_button("Music",   self.shell.musicScreen),
                self.screen_button("ListBox", self.shell.listBoxScreen),
                self.screen_button("User Events", self.shell.userEventsScreen)
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

        # buttFont = ResourceUtility.get_font(DEMO_BUTTON_TEXT_SIZE, Theme.BUILT_IN_FONT)
        # buttAttrs = {
        #     'font': buttFont
        # }
        retButton = Button(text, action=lambda: self.shell.show_screen(screen))
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

    def __repr__(self):
        return self.__class__.__name__
