
import logging

from logging import Logger

import pygame
from pygame.event import Event
from pygame.font import Font

from albow.core.ui.RootWidget import RootWidget
from albow.core.ui.Shell import Shell
from albow.core.UserEventCall import UserEventCall
from albow.core.ResourceUtility import ResourceUtility

from albow.themes.Theme import Theme

from albow.layout.Column import Column

from albow.widgets.TextBox import TextBox
from albow.widgets.Label import Label

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoUserEventsScreen(BaseDemoScreen):

    CLOCK_EVENT = RootWidget.MUSIC_END_EVENT + 1
    KLINGON_TORPEDO_EVENT = CLOCK_EVENT + 1

    classLogger: Logger = None
    classTextBox: TextBox = None
    classLineCounter: int = 0

    def __init__(self, shell: Shell):

        super().__init__(shell)

        self.logger = logging.getLogger(__name__)
        DemoUserEventsScreen.classLogger = self.logger

        DemoUserEventsScreen.classTextBox = TextBox()

        f1: Font = ResourceUtility.get_font(16, Theme.BUILT_IN_BOLD_FONT)
        textBoxTitle: Label = Label(text="User Events", font=f1)

        contentAttrs = {
            "align": "c"
        }
        contents: Column = Column([textBoxTitle, DemoUserEventsScreen.classTextBox, self.backButton], **contentAttrs)

        clockEventCall: UserEventCall = UserEventCall(func=DemoUserEventsScreen.userEventCallback, userEvent=DemoUserEventsScreen.CLOCK_EVENT)
        ktkEventCall: UserEventCall = UserEventCall(func=DemoUserEventsScreen.userEventCallback, userEvent=DemoUserEventsScreen.KLINGON_TORPEDO_EVENT)

        RootWidget.addUserEvent(clockEventCall)
        RootWidget.addUserEvent(ktkEventCall)
        self.add_centered(contents)

    def enter_screen(self):
        """
        Called from the Shell after switching to this screen from another screen.
        """
        self.logger.debug("Start timers")
        pygame.time.set_timer(DemoUserEventsScreen.CLOCK_EVENT, 5 * 1000)
        pygame.time.set_timer(DemoUserEventsScreen.KLINGON_TORPEDO_EVENT, 7 * 1000)

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
