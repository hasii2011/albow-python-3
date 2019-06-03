
from typing import Callable

import logging

from logging import Logger

from pygame import Surface

from pygame.event import Event

from albow.core.ui.Shell import Shell
from albow.core.ui.Widget import Widget
from albow.core.ui.Screen import Screen

from albow.containers.TabPanel import TabPanel

from albow.layout.Column import Column
from albow.layout.Frame import Frame

from albow.demo.screens.DemoControlsScreen import DemoControlsScreen
from albow.demo.screens.DemoTextFieldsScreen import DemoTextFieldsScreen
from albow.demo.screens.DemoDialogScreen import DemoDialogScreen
from albow.demo.screens.DemoMultiChoiceScreen import DemoMultiChoiceScreen
from albow.demo.screens.DemoImageArrayScreen import DemoImageArrayScreen
from albow.demo.screens.DemoListBoxScreen import DemoListBoxScreen
from albow.demo.screens.DemoUserEventsScreen import DemoUserEventsScreen


class AlbowDemoScreen(Screen):

    demoTabs = [
        ('Controls', DemoControlsScreen.makeContents),
        ('Text Fields', DemoTextFieldsScreen.makeContents),
        ('Dialogs', DemoDialogScreen.makeContents),
        ("MultiChoice", DemoMultiChoiceScreen.makeContents),
        ("Image Array", DemoImageArrayScreen.makeContents),
        ("Events", DemoUserEventsScreen.makeContents)
    ]
    EVENT_TAB_IDX = 5

    classLogger: Logger = None

    def __init__(self, shell: Shell, theSurface: Surface):

        super().__init__(shell)

        self.logger = logging.getLogger(__name__)
        self.surface = theSurface
        AlbowDemoScreen.classLogger = self.logger

        width = shell.width - (shell.margin * 2)
        height = shell.height - (shell.margin * 2)
        tabPanel = TabPanel(width=width, height=height, enterTabAction=AlbowDemoScreen.enterTabAction, exitTabAction=AlbowDemoScreen.exitTabAction)

        self.tabPanel = tabPanel
        for tabInfo in AlbowDemoScreen.demoTabs:

            tabLabel: str = tabInfo[0]
            tabFunc: Callable = tabInfo[1]
            tabContents: Widget = tabFunc()
            frame: Frame = Frame(client=tabContents, margin=10)
            tabPanel.add_page(tabLabel, frame)
        #
        #  'Special' tab
        #
        specialContents: Column = DemoListBoxScreen.makeContents(client=self)
        specialFrame: Frame = Frame(client=specialContents, margin=10)

        tabPanel.add_page("List Box", specialFrame)

        #
        # Special Setup
        #
        DemoUserEventsScreen.setupUserEvents()

        self.add(tabPanel)

    @classmethod
    def enterTabAction(cls, theEvent: Event):

        cls.classLogger.debug(f"Enter event index: {theEvent.index}")
        if theEvent.index == AlbowDemoScreen.EVENT_TAB_IDX:
            DemoUserEventsScreen.initializeUserEvents()


    @classmethod
    def exitTabAction(cls, theEvent: Event):

        cls.classLogger.debug(f"Enter event index: {theEvent.index}")
        if theEvent.index == AlbowDemoScreen.EVENT_TAB_IDX:
            DemoUserEventsScreen.resetUserEvents()
