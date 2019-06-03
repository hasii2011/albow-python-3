
import logging

from logging import Logger

import pygame
from pygame.event import Event
from pygame.font import Font

from albow.core.ui.RootWidget import RootWidget
from albow.core.ui.AlbowEventLoop import AlbowEventLoop

from albow.core.ui.Shell import Shell

from albow.core.UserEventCall import UserEventCall
from albow.core.ResourceUtility import ResourceUtility

from albow.themes.Theme import Theme

from albow.layout.Column import Column

from albow.widgets.TextBox import TextBox
from albow.widgets.Label import Label
from albow.widgets.Button import Button

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoUserEventsScreen(BaseDemoScreen):

    CLOCK_EVENT = AlbowEventLoop.MUSIC_END_EVENT + 1
    KLINGON_TORPEDO_EVENT = CLOCK_EVENT + 1

    classLogger: Logger = logging.getLogger(__name__)
    classTextBox: TextBox = None
    classLineCounter: int = 0

    def __init__(self, shell: Shell):

        super().__init__(shell)

        self.logger = DemoUserEventsScreen.classLogger
        DemoUserEventsScreen.classLogger = self.logger

        contents = DemoUserEventsScreen.makeContents(self.backButton)
        self.setupUserEvents()
        self.add_centered(contents)

    def enter_screen(self):
        """
        Called from the Shell after switching to this screen from another screen.
        """
        self.logger.debug("Start timers")
        self.initializeUserEvents()

    def leave_screen(self):
        """
        Called from the Shell before switching away from this screen to another screen.
        """
        #
        # From the pygame official documentation
        #
        #   To disable the timer for an event, set the milliseconds argument to 0.
        #
        self.logger.debug("Stop timers")
        self.resetUserEvents()

    @classmethod
    def makeContents(cls, backButton: Button = None) -> Column:

        DemoUserEventsScreen.classTextBox = TextBox()

        f1: Font = ResourceUtility.get_font(16, Theme.BUILT_IN_BOLD_FONT)
        textBoxTitle: Label = Label(text="User Events", font=f1)

        contentAttrs = {
            "align": "c"
        }
        if backButton is None:
            contents: Column = Column([textBoxTitle, DemoUserEventsScreen.classTextBox], **contentAttrs)
        else:
            contents: Column = Column([textBoxTitle, DemoUserEventsScreen.classTextBox, backButton], **contentAttrs)

        return contents

    @classmethod
    def setupUserEvents(cls):

        clockEventCall: UserEventCall = UserEventCall(func=DemoUserEventsScreen.userEventCallback, userEvent=DemoUserEventsScreen.CLOCK_EVENT)
        ktkEventCall: UserEventCall = UserEventCall(func=DemoUserEventsScreen.userEventCallback, userEvent=DemoUserEventsScreen.KLINGON_TORPEDO_EVENT)
        RootWidget.addUserEvent(clockEventCall)
        RootWidget.addUserEvent(ktkEventCall)

    @classmethod
    def initializeUserEvents(cls):

        pygame.time.set_timer(DemoUserEventsScreen.CLOCK_EVENT, 5 * 1000)
        pygame.time.set_timer(DemoUserEventsScreen.KLINGON_TORPEDO_EVENT, 7 * 1000)
        cls.classLineCounter = 0
        cls.classTextBox.set_text("")

    @classmethod
    def resetUserEvents(cls):
        pygame.time.set_timer(DemoUserEventsScreen.CLOCK_EVENT, 0)
        pygame.time.set_timer(DemoUserEventsScreen.KLINGON_TORPEDO_EVENT, 0)

    @staticmethod
    def userEventCallback(theEvent: Event):

        timeMSecs: float = theEvent.dict['time']
        timeSecs: float = timeMSecs // 1000

        lineCounter = DemoUserEventsScreen.classLineCounter

        cbText: str = f"{str(lineCounter)}: type: '{theEvent.type}' - time: {timeSecs}"
        DemoUserEventsScreen.classLogger.debug(cbText)

        oldText = DemoUserEventsScreen.classTextBox.get_text()
        cbText = f"{oldText}\n{cbText}"

        DemoUserEventsScreen.classLineCounter += 1
        DemoUserEventsScreen.classTextBox.set_text(cbText)
