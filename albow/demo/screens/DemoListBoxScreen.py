
import logging

from albow.core.ResourceUtility import ResourceUtility

from albow.core.Shell import Shell

from albow.layout.Column import Column

from albow.themes.Theme import Theme

from albow.widgets.Label import Label
from albow.widgets.ListBox import ListBox

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen

DEMO_LIST_DATA = [
    "Humberto", "Fran", "Opie", "Gabriel"
]

DEMO_LABEL_TEXT_SIZE = 18


class DemoListBoxScreen(BaseDemoScreen):

    selectedLabel: Label = None

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)

        super().__init__(shell=shell)

        labelFont = ResourceUtility.get_font(DEMO_LABEL_TEXT_SIZE, Theme.BUILT_IN_FONT)

        labelAttrs = {
            "bg_color": Theme.WHITE,
            "fg_color": Theme.BLACK
        }
        demoListBoxLabel:   Label   = Label(text="Pick a good guy", font=labelFont, **labelAttrs)
        demoListBox:        ListBox = ListBox(theClient=self, theItems=DEMO_LIST_DATA, selectAction=self.selectAction)
        self.selectedLabel: Label   = Label(text="No selection", **labelAttrs)
        columnAttrs = {
            "align": "c",
            'expand': 0
        }

        contents = Column([demoListBoxLabel,
                           demoListBox,
                           self.selectedLabel,
                           self.backButton], **columnAttrs)
        self.add_centered(contents)
        self.backButton.focus()

    def selectAction(self, theSelectedItem: str):

        self.logger.info("Selected item: %s", theSelectedItem)
        self.selectedLabel.set_text(theSelectedItem)

