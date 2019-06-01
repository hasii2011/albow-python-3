
import logging

from albow.core.ResourceUtility import ResourceUtility

from albow.themes.Theme import Theme

from albow.core.ui.Screen import Screen
from albow.core.ui.Shell import Shell

from albow.widgets.Button import Button


class BaseDemoScreen(Screen):

    SMALL_BUTTON_TEXT_SIZE:  int = 14
    SMALL_LABEL_TEXT_SIZE:   int = 14
    DEFAULT_CONTENT_SPACING: int = 30

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)

        super().__init__(shell=shell)

        self.smallButtonFont = ResourceUtility.get_font(BaseDemoScreen.SMALL_BUTTON_TEXT_SIZE, Theme.BUILT_IN_FONT)
        self.labelFont       = ResourceUtility.get_font(BaseDemoScreen.SMALL_LABEL_TEXT_SIZE, Theme.BUILT_IN_FONT)

        self.backButton      = Button("Back", action=shell.show_menu, font=self.smallButtonFont)
