
import logging
from logging import Logger

from pygame.font import Font

from albow.core.Scheduler import Scheduler
from albow.core.ScheduledCall import ScheduledCall

from albow.core.ui.Widget import Widget

from albow.core.ResourceUtility import ResourceUtility

from albow.themes.Theme import Theme

from albow.layout.Column import Column

from albow.widgets.TextBox import TextBox
from albow.widgets.Label import Label


class ScheduledEventTabPage(Widget):

    DELAY_3_SECS = 3 * 1000
    DELAY_6_SECS = 6 * 1000
    REPEAT = True

    def __init__(self, **kwds):

        super().__init__(**kwds)

        self.logger = logging.getLogger(__name__)
        self.textBox = TextBox()

        f1: Font = ResourceUtility.get_font(16, Theme.BUILT_IN_BOLD_FONT)
        textBoxTitle: Label = Label(text="Scheduled Events", font=f1)

        contentAttrs = {
            'align': 'c'
        }

        contents: Column = Column([textBoxTitle, self.textBox], **contentAttrs)
        self.token3 = None
        self.token6 = None
        self.add_centered(contents)

    def createScheduledEvents(self):

        self.token3: ScheduledCall = Scheduler.schedule_call(delay=ScheduledEventTabPage.DELAY_3_SECS,
                                                             func=self.scheduledMethod,
                                                             repeat=ScheduledEventTabPage.REPEAT)

        self.token6: ScheduledCall = Scheduler.schedule_call(delay=ScheduledEventTabPage.DELAY_3_SECS,
                                                             func=self.scheduledMethod,
                                                            repeat=ScheduledEventTabPage.REPEAT)

    def cancelScheduledEvents(self):

        Scheduler.cancel_call(token=self.token3)
        Scheduler.cancel_call(token=self.token6)

    def scheduledMethod(self):

        ts = Scheduler.timestamp()
        cbText = f"I have been called at: {ts}"
        self.logger.info(cbText)

        oldText = self.textBox.get_text()

        cbText = f"{oldText}\n{cbText}"

        self.textBox.set_text(cbText)
