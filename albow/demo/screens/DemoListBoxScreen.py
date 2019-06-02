
import logging
from logging import Logger

from albow.core.ResourceUtility import ResourceUtility

from albow.core.ui.Shell import Shell
from albow.core.ui.Widget import Widget

from albow.layout.Column import Column

from albow.themes.Theme import Theme

from albow.widgets.Label import Label
from albow.widgets.Button import Button
from albow.widgets.ListBox import ListBox

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoListBoxScreen(BaseDemoScreen):

    DEMO_LIST_DATA = [
        "Humberto", "Fran", "Opie", "Gabriel (Gabby10Meows)"
    ]

    DEMO_LABEL_TEXT_SIZE = 18

    selectedLabel: Label = None
    logger: Logger = logging.getLogger(__name__)

    def __init__(self, shell: Shell):

        super().__init__(shell=shell)

        contents = DemoListBoxScreen.makeContents(client=self, backButton=self.backButton)
        self.add_centered(contents)
        self.backButton.focus()

    @classmethod
    def makeContents(cls, client: Widget, backButton: Button=None) -> Column:

        labelFont = ResourceUtility.get_font(DemoListBoxScreen.DEMO_LABEL_TEXT_SIZE, Theme.BUILT_IN_FONT)

        demoListBoxLabel: Label = Label(text="Pick a good guy", font=labelFont)

        demoListBox: ListBox = ListBox(theClient=client, theItems=DemoListBoxScreen.DEMO_LIST_DATA, selectAction=cls.selectAction)

        cls.selectedLabel: Label = Label(text="No selection")
        lbColumnAttrs = {
            "align": "c",
            'expand': 0
        }
        listBoxColumn = Column([demoListBoxLabel, demoListBox], **lbColumnAttrs)

        columnAttrs = {
            "align": "l",
            'expand': 0
        }
        if backButton is None:
            contents = Column([listBoxColumn, cls.selectedLabel], **columnAttrs)
        else:
            contents = Column([listBoxColumn,
                               cls.selectedLabel,
                               backButton], **columnAttrs)
        return contents

    @classmethod
    def selectAction(cls, theSelectedItem: str):

        cls.logger.info("Selected item: %s", theSelectedItem)
        cls.selectedLabel.set_text(theSelectedItem)
