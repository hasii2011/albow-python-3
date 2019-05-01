
import logging

from albow.themes.Theme import Theme

from albow.core.Screen import Screen
from albow.core.Shell import Shell

from albow.widgets.Button import Button

class BaseDemoScreen(Screen):

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)

        screenAttrs = {'bg_color': Theme.WHITE}

        super().__init__(shell=shell, **screenAttrs)

        self.backButton = Button("Back", action=shell.show_menu)

