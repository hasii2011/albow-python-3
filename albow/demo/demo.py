"""
    Albow - Demonstration
"""
import os
import sys

from os.path import dirname as d

import pygame
import logging.config


from albow.shell import Shell
from albow.text_screen import TextScreen


from albow.themes.Theme import Theme

from albow.demo.screens.DemoMultiChoiceScreen import DemoMultiChoiceScreen
from albow.demo.screens.DemoTableScreen import DemoTableScreen
from albow.demo.screens.DemoTabPanelScreen import DemoTabPanelScreen
from albow.demo.screens.DemoGridViewScreen import DemoGridViewScreen
from albow.demo.screens.DemoPaletteViewScreen import DemoPaletteViewScreen
from albow.demo.screens.DemoImageArrayScreen import DemoImageArrayScreen
from albow.demo.screens.DemoAnimationScreen import DemoAnimationScreen
from albow.demo.screens.DemoControlsScreen import DemoControlsScreen
from albow.demo.screens.DemoTextFieldsScreen import DemoTextFieldsScreen
from albow.demo.screens.DemoDialogScreen import DemoDialogScreen
from albow.demo.screens.MenuScreen import MenuScreen

# SCREEN_SIZE   = (640, 480)
# DISPLAY_FLAGS = pygame.RESIZABLE
SCREEN_SIZE = (480, 640)
DISPLAY_FLAGS    = 0
DEMO_FRAME_TIME  = 50  # ms

sys.path.insert(1, d(d(os.path.abspath(sys.argv[0]))))


class DemoShell(Shell):
    """
    Shell
    """
    def __init__(self, display):
        """

        :param display:
        """
        #
        # Python 3 update
        #
        attrs = {'bg_color': Theme.WHITE}
        super().__init__(display, **attrs)

        self.text_screen        = TextScreen(self, "demo_text.txt")
        self.fields_screen      = DemoTextFieldsScreen(self)
        self.controls_screen    = DemoControlsScreen(self)
        self.anim_screen        = DemoAnimationScreen(self)
        self.grid_screen        = DemoGridViewScreen(self)
        self.palette_screen     = DemoPaletteViewScreen(self)
        self.image_array_screen = DemoImageArrayScreen(self)
        self.dialog_screen      = DemoDialogScreen(self)
        self.tab_panel_screen   = DemoTabPanelScreen(self)
        self.table_screen       = DemoTableScreen(self)
        self.multiChoiceScreen  = DemoMultiChoiceScreen(self)

        self.menu_screen = MenuScreen(self)  # Do this last
        self.set_timer(DEMO_FRAME_TIME)
        self.show_menu()

    def show_menu(self):
        self.show_screen(self.menu_screen)


def main():

    pygame.init()
    pygame.display.set_caption("Albow Demonstration")

    logging.config.fileConfig('logging.conf')

    logger  = logging.getLogger(__name__)
    display = pygame.display.set_mode(SCREEN_SIZE, DISPLAY_FLAGS)
    shell   = DemoShell(display)

    logger.info("Starting %s", __name__)

    shell.run()


main()
