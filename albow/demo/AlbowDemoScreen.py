
from typing import Callable

import logging

from pygame import Surface

from albow.core.ui.Shell import Shell
from albow.core.ui.Widget import Widget
from albow.core.ui.Screen import Screen

from albow.containers.TabPanel import TabPanel

from albow.layout.Row import Row
from albow.layout.Frame import Frame

from albow.demo.screens.DemoControlsScreen import DemoControlsScreen
from albow.demo.screens.DemoTextFieldsScreen import DemoTextFieldsScreen
from albow.demo.screens.DemoDialogScreen import DemoDialogScreen
from albow.demo.screens.DemoMultiChoiceScreen import DemoMultiChoiceScreen
from albow.demo.screens.DemoImageArrayScreen import DemoImageArrayScreen


class AlbowDemoScreen(Screen):

    tabLabels = [
        'Controls',
        'Text',
        'Dialogs',
        'Events',
        'Views',
    ]
    demoTabs = [
        ('Controls', DemoControlsScreen.makeContents),
        ('Text Fields', DemoTextFieldsScreen.makeContents),
        ('Dialogs', DemoDialogScreen.makeContents),
        ("MultiChoice", DemoMultiChoiceScreen.makeContents),
        ("Image Array", DemoImageArrayScreen.makeContents)
    ]

    def __init__(self, shell: Shell, theSurface: Surface):

        super().__init__(shell)

        self.logger = logging.getLogger(__name__)
        self.surface = theSurface

        width = shell.width - (shell.margin * 2)
        height = shell.height - (shell.margin * 2)
        tabPanel = TabPanel(width=width, height=height)

        self.tabPanel = tabPanel
        for tabInfo in AlbowDemoScreen.demoTabs:

            tabLabel: str = tabInfo[0]
            tabFunc: Callable = tabInfo[1]
            tabContents: Widget = tabFunc()
            frame: Frame = Frame(client=tabContents, margin=10)
            tabPanel.add_page(tabLabel, frame)

        contents = Row([tabPanel], margin=5)

        self.add(contents)
