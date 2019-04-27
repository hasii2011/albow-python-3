"""
    Albow - Demonstration
"""
import os
import sys

from os.path import dirname as d

import pygame
import logging.config

from albow.widgets.Label import Label

from albow.widgets.Button import Button

from albow.layout.Column import Column

from albow.shell import Shell
from albow.screen import Screen
from albow.text_screen import TextScreen
from albow.resource import get_font


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

# screen_size = (640, 480)
screen_size = (480, 640)

flags       = 0
frame_time  = 50  # ms

sys.path.insert(1, d(d(os.path.abspath(sys.argv[0]))))


class MenuScreen(Screen):
    """
    Buttons
    """

    def __init__(self, shell):
        """

        :param shell:
        """
        #
        # Python 3 update
        #
        # Screen.__init__(self, shell)
        super().__init__(shell)

        self.shell     = shell
        f1             = get_font(24, "VeraBd.ttf")
        title          = Label("Albow Demonstration", font = f1)
        title.fg_color = (255, 255, 255)


        menu = Column([
            self.screen_button("Text Screen",    shell.text_screen),
            self.screen_button("Text Fields",    shell.fields_screen),
            self.screen_button("Controls",       shell.controls_screen),
            self.screen_button("Timing",         shell.anim_screen),
            self.screen_button("Grid View",      shell.grid_screen),
            self.screen_button("Palette View",   shell.palette_screen),
            self.screen_button("Image Array",    shell.image_array_screen),
            self.screen_button("Modal Dialogs",  shell.dialog_screen),
            self.screen_button("Tab Panel",      shell.tab_panel_screen),
            self.screen_button("Table View",     shell.table_screen),
            self.screen_button("MultiChoice",    shell.multiChoiceScreen),
            Button("Quit", shell.quit),
        ], align='l')
        contents = Column([
            title,
            menu,
        ], align = 'l', spacing=20)
        self.add_centered(contents)

    def screen_button(self, text: str, screen: Screen):
        return Button(text, action=lambda: self.shell.show_screen(screen))

    def show_text_screen(self):
        self.shell.show_screen(self.text_screen)

    def show_fields_screen(self):
        self.shell.show_screen(self.fields_screen)
        self.fields_screen.fld1.focus()

    def show_animation_screen(self):
        self.shell.show_screen(self.anim_screen)

    def quit(self):
        sys.exit(0)

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
        self.set_timer(frame_time)
        self.show_menu()

    def show_menu(self):
        self.show_screen(self.menu_screen)

    def begin_frame(self):
        self.anim_screen.begin_frame()


def main():

    pygame.init()
    pygame.display.set_caption("Albow Demonstration")

    logging.config.fileConfig('logging.conf')

    logger  = logging.getLogger(__name__)
    display = pygame.display.set_mode(screen_size, flags)
    shell   = DemoShell(display)

    logger.info("Starting %s", __name__)

    shell.run()


main()
