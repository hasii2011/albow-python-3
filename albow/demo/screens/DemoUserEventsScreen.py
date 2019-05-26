
import logging

from logging import Logger

import pygame
from pygame.event import Event

from albow.core.RootWidget import RootWidget
from albow.core.Shell import Shell
from albow.core.UserEventCall import UserEventCall

from albow.layout.Column import Column

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoUserEventsScreen(BaseDemoScreen):

    CLOCK_EVENT = RootWidget.MUSIC_END_EVENT + 1
    KLINGON_TORPEDO_EVENT = CLOCK_EVENT + 1

    classLogger: Logger = None

    def __init__(self, shell: Shell):

        super().__init__(shell)

        self.logger = logging.getLogger(__name__)
        DemoUserEventsScreen.classLogger = self.logger

        contentAttrs = {
            "align": "c"
        }

        contents: Column = Column([self.backButton], **contentAttrs)

        clockEventCall: UserEventCall = UserEventCall(func=DemoUserEventsScreen.userEventCallback, userEvent=DemoUserEventsScreen.CLOCK_EVENT)
        ktkEventCall: UserEventCall = UserEventCall(func=DemoUserEventsScreen.userEventCallback, userEvent=DemoUserEventsScreen.KLINGON_TORPEDO_EVENT)

        RootWidget.addUserEvent(clockEventCall)
        RootWidget.addUserEvent(ktkEventCall)
        self.add_centered(contents)

    def enter_screen(self):
        """
        Called from the Shell after switching to this screen from another screen.
        """
        self.logger.info("Start timers")
        pygame.time.set_timer(DemoUserEventsScreen.CLOCK_EVENT, 10 * 1000)
        pygame.time.set_timer(DemoUserEventsScreen.KLINGON_TORPEDO_EVENT, 15 * 1000)

    def leave_screen(self):
        """
        Called from the Shell before switching away from this screen to another screen.
        """
        #
        # From the pygame official documentation
        #
        #   To disable the timer for an event, set the milliseconds argument to 0.
        #
        self.logger.info("Stop timers")
        pygame.time.set_timer(DemoUserEventsScreen.CLOCK_EVENT, 0)
        pygame.time.set_timer(DemoUserEventsScreen.KLINGON_TORPEDO_EVENT, 0)

    @staticmethod
    def userEventCallback(theEvent: Event):

        timeMSecs: float = theEvent.dict['time']
        timeSecs: float = timeMSecs // 1000
        DemoUserEventsScreen.classLogger.info(f"theEvent.type: '{theEvent.type}, time(seconds) since start: {timeSecs}")
