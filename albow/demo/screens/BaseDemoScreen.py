
import logging

from albow.core.ResourceUtility import ResourceUtility

from albow.themes.Theme import Theme

from albow.core.Screen import Screen
from albow.core.Shell import Shell

from albow.widgets.Button import Button


class BaseDemoScreen(Screen):

    SMALL_BUTTON_TEXT_SIZE:  int = 14
    SMALL_LABEL_TEXT_SIZE:   int = 14
    DEFAULT_CONTENT_SPACING: int = 30

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)

        screenAttrs = {'bg_color': Theme.WHITE}

        super().__init__(shell=shell, **screenAttrs)

        self.smallButtonFont = ResourceUtility.get_font(BaseDemoScreen.SMALL_BUTTON_TEXT_SIZE, Theme.BUILT_IN_FONT)
        self.backButton      = Button("Back", action=shell.show_menu)
        self.labelFont       = ResourceUtility.get_font(BaseDemoScreen.SMALL_LABEL_TEXT_SIZE, Theme.BUILT_IN_FONT)

        self.labelAttrs = {
            "bg_color": Theme.WHITE,
            "fg_color": Theme.BLACK
        }
