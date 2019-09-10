
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


class GridDebugScreen(Screen):
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
                self.screen_button("R0C0"),
                self.screen_button("R0C1"),
                self.screen_button("R0C2"),
            ],
            # [
            #     self.screen_button("R1C0"),
            #     self.screen_button("R1Column1"),
            #     self.screen_button("R1C2"),
            # ],
            # [
            #     self.screen_button("R2C0"),
            #     self.screen_button("R2Column1"),
            #     self.screen_button("R2C2"),
            # ],
            # [
            #     self.screen_button("R3C0"),
            #     self.screen_button("R3Column1"),
            #     self.screen_button("R3C2")
            # ],
            # [
            #     self.screen_button("R4C0"),
            #     self.screen_button("R4Column1"),
            #     self.screen_button("R4C2")
            # ]
        ]

        menuGrid = Grid(rows=menuArray, column_spacing=10, row_spacing=2, margin=5)
        quitButton = Button("Quit", shell.quit)

        self.equallySizeButtons(menuArray)

        contents = Column([
            title,
            menuGrid,
            quitButton
        ], align='c', spacing=10, border_width=1, border_color=Theme.BLUE, margin=10)
        self.add_centered(contents)

    def screen_button(self, text: str):

        retButton = Button(text)
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
