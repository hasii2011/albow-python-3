
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
from albow.layout.Row import Row
from albow.layout.Frame import Frame

from albow.widgets.Label import Label

from albow.demo.screens.DemoControlsScreen import DemoControlsScreen
from albow.demo.screens.DemoTextFieldsScreen import DemoTextFieldsScreen
from albow.demo.screens.DemoDialogScreen import DemoDialogScreen
from albow.demo.screens.DemoMultiChoiceScreen import DemoMultiChoiceScreen
from albow.demo.screens.DemoImageArrayScreen import DemoImageArrayScreen
from albow.demo.screens.DemoListBoxScreen import DemoListBoxScreen
from albow.demo.screens.DemoUserEventsScreen import DemoUserEventsScreen
from albow.demo.screens.DemoAnimationWidget import DemoAnimationWidget

from albow.demo.ScheduledEventTabPage import ScheduledEventTabPage

from albow.demo.views.DemoTableView import DemoTableView
from albow.demo.views.DemoGridView import DemoGridView
from albow.demo.views.DemoPaletteView import DemoPaletteView

class AlbowDemoScreen(Screen):

    demoTabs = [
        ('Controls', DemoControlsScreen.makeContents),
        ('Text Fields', DemoTextFieldsScreen.makeContents),
        ('Dialogs', DemoDialogScreen.makeContents),
        ("MultiChoice", DemoMultiChoiceScreen.makeContents),
        ("Image Array", DemoImageArrayScreen.makeContents)
    ]
    EVENT_TAB_IDX = 6

    classLogger: Logger = None
    classScheduledEventsTabPage: ScheduledEventTabPage = None

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

        self._makeSpecialTabs(tabPanel)
        #
        # Special Setup
        #
        DemoUserEventsScreen.setupUserEvents()
        self.add(tabPanel)

    def _makeSpecialTabs(self, tabPanel: TabPanel):

        self._makeListBoxTab(tabPanel)
        self._makeEventsTab(tabPanel)
        self._makeAnimationTab(tabPanel)
        self._makeGridLikeTab(tabPanel)

    def _makeListBoxTab(self, tabPanel):

        specialContents: Column = DemoListBoxScreen.makeContents(client=self)
        specialFrame: Frame = Frame(client=specialContents, margin=10)
        tabPanel.add_page("List Box", specialFrame)

    def _makeEventsTab(self, tabPanel):

        userEvents: Column = DemoUserEventsScreen.makeContents()
        scheduledEventsTabPage: ScheduledEventTabPage = ScheduledEventTabPage(height=userEvents.height, width=userEvents.width)
        contentAttrs = {
            'align' : "c",
            'margin': 10
        }
        eventTab: Column = Column([userEvents, scheduledEventsTabPage], **contentAttrs)
        tabPanel.add_page("Events", eventTab)
        AlbowDemoScreen.classScheduledEventsTabPage = scheduledEventsTabPage

    def _makeAnimationTab(self, tabPanel):

        animationWidget: DemoAnimationWidget = DemoAnimationWidget(self.shell)
        tabPanel.add_page("Animation", animationWidget)

    def _makeGridLikeTab(self, tabPanel):

        gridTabAttrs = {
            'align' : "c",
            'margin': 20
        }

        grid: DemoGridView = DemoGridView()
        lbl         = Label("Cl1ck a Squ4r3")
        grid.output = lbl
        # gridColAttrs = {'margin': 10}
        gridColumn: Column = Column([grid, lbl])

        table: DemoTableView = DemoTableView()
        palette: DemoPaletteView = DemoPaletteView()

        gridTab: Row = Row([table, palette, gridColumn], **gridTabAttrs)
        tabPanel.add_page("Grids", gridTab)

    @classmethod
    def enterTabAction(cls, theEvent: Event):

        cls.classLogger.debug(f"Enter event index: {theEvent.index}")
        if theEvent.index == AlbowDemoScreen.EVENT_TAB_IDX:
            DemoUserEventsScreen.initializeUserEvents()
            if cls.classScheduledEventsTabPage is not None:
                cls.classScheduledEventsTabPage.createScheduledEvents()

    @classmethod
    def exitTabAction(cls, theEvent: Event):

        cls.classLogger.info(f"Enter event index: {theEvent.index}")
        if theEvent.index == AlbowDemoScreen.EVENT_TAB_IDX:
            DemoUserEventsScreen.resetUserEvents()
            if cls.classScheduledEventsTabPage is not None:
                cls.classScheduledEventsTabPage.cancelScheduledEvents()
