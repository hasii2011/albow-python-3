"""
    Albow - Demonstration
"""
import os
import sys

from os.path import dirname as d

import pygame
import logging.config

# from pygame.locals import *

from albow.widgets.Label import Label

from albow.widgets.Button import Button

from albow.layout.Column import Column

from albow.input.TextField import TextField

from albow.shell import Shell
from albow.screen import Screen
from albow.text_screen import TextScreen
from albow.resource import get_font

from albow.dialog.DialogUtilities import alert
from albow.dialog.DialogUtilities import ask

from albow.dialog.FileDialogUtilities import request_old_filename
from albow.dialog.FileDialogUtilities import request_new_filename
from albow.dialog.FileDialogUtilities import look_for_file_or_directory

from albow.themes.Theme import Theme

from albow.demo.screens.DemoMultiChoiceScreen import DemoMultiChoiceScreen
from albow.demo.screens.DemoTableScreen import DemoTableScreen
from albow.demo.screens.DemoTabPanelScreen import DemoTabPanelScreen
from albow.demo.screens.DemoGridViewScreen import DemoGridViewScreen
from albow.demo.screens.DemoPaletteViewScreen import DemoPaletteViewScreen
from albow.demo.screens.DemoImageArrayScreen import DemoImageArrayScreen
from albow.demo.screens.DemoAnimationScreen import DemoAnimationScreen
from albow.demo.screens.DemoControlsScreen import DemoControlsScreen

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


class DemoTextFieldsScreen(Screen):
    """
    Text Field
    """

    def __init__(self, shell):
        """

        :param shell:
        """
        attrs = {'bg_color': Theme.WHITE}
        #
        # Python 3 update
        #
        # Screen.__init__(self, shell)
        super().__init__(shell, **attrs)

        self.fld1 = self.add_field("Name", 200)
        self.fld2 = self.add_field("Race", 250)
        btn = Button("OK", action=self.ok)
        btn.rect.midtop = (320, 300)
        self.add(btn)
        out = Label("")
        out.rect.width = 400
        out.rect.topleft = (200, 350)
        self.out = out
        self.add(out)
        btn = Button("Menu", action=self.go_back)
        btn.rect.midtop = (320, 400)
        self.add(btn)
        self.fld1.focus()

    def add_field(self, label, pos):
        """

        :param label:
        :param pos:
        :return:
        """
        lbl = Label(label)
        lbl.rect.topleft = (200, pos)
        self.add(lbl)
        fld = TextField(150)
        fld.rect.topleft = (250, pos)
        fld.enter_action = self.ok
        self.add(fld)
        return fld

    def ok(self):
        self.out.text = "You are a %s called %s." % (self.fld2.text, self.fld1.text)

    def go_back(self):
        self.parent.show_menu()


class DemoDialogScreen(Screen):
    """
    Dialogs
    """

    def __init__(self, shell):
        Screen.__init__(self, shell)
        menu = Column([
            Button("Ask a Question",             self.test_ask),
            Button("Request Old Filename",       self.test_old),
            Button("Request New Filename",       self.test_new),
            Button("Look for File or Directory", self.test_lookfor),
        ], align='l')
        contents = Column([
            Label("File Dialogs", font=get_font(18, "VeraBd.ttf")),
            menu,
            Button("Menu", action=shell.show_menu),
        ], align='l', spacing=30)
        self.add_centered(contents)

    def test_ask(self):
        response = ask("Do you like mustard and avocado ice cream?",["Yes", "No", "Undecided"])
        alert("You chose %r." % response)

    def test_old(self):
        path = request_old_filename()
        if path:
            alert("You chose %r." % path)
        else:
            alert("Cancelled.")

    def test_new(self):
        path = request_new_filename(prompt="Save booty as:", filename="treasure", suffix=".dat")
        if path:
            alert("You chose %r." % path)
        else:
            alert("Cancelled.")

    def test_lookfor(self):
        path = look_for_file_or_directory(prompt="Please find 'Vera.ttf'", target="Vera.ttf")
        if path:
            alert("You chose %r." % path)
        else:
            alert("Cancelled.")


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
        super().__init__(display,**attrs)

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
