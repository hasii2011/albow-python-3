
import logging

from pygame import Surface
from albow.core.ui.Shell import Shell

from albow.core.ui.Widget import Widget
from albow.core.ui.Screen import Screen

from albow.containers.TabPanel import TabPanel

from albow.layout.Row import Row
from albow.widgets.Label import Label


class AlbowDemoScreen(Screen):

    tabLabels = [
        'Controls',
        'Text',
        'Dialogs',
        'Events',
        'Views',
    ]
    def __init__(self, shell: Shell, theSurface: Surface):

        super().__init__(shell)

        self.logger = logging.getLogger(__name__)
        self.surface = theSurface

        width = shell.width - (shell.margin * 2)
        height = shell.height - (shell.margin * 2)
        tabPanel = TabPanel(width=width, height=height)
        # tabPanel.size = 400, 200
        self.pages = tabPanel

        #for i in range(1, 4):
        for tabText in AlbowDemoScreen.tabLabels:
            page = self.makeTestPage(tabText)
            tabPanel.add_page(tabText, page)

        contents = Row([tabPanel], margin=5)

        self.add(contents)
        # self.add_centered(contents)

    def makeTestPage(self, pageLabel: str) -> Widget:

        page_size = self.pages.content_size()
        page = Widget(size=page_size, border_width=1)
        lbl = Label(f"{pageLabel}")
        page.add_centered(lbl)

        return page
