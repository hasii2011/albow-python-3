
import sys

from albow.resource import get_font
from albow.screen import Screen
from albow.shell import Shell

from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.layout.Column import Column

from albow.themes.Theme import Theme

class MenuScreen(Screen):
    """
    Buttons
    """

    def __init__(self, shell: Shell):
        """

        :param shell:
        """
        #
        # Python 3 update
        #
        # Screen.__init__(self, shell)
        super().__init__(shell)

        self.shell     = shell
        f1             = get_font(24, Theme.BUILT_IN_FONT)
        title          = Label("Albow Demonstration", font = f1)
        title.fg_color = Theme.WHITE


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
            # self.screen_button("MultiChoice",    shell.multiChoiceScreen),
            Button("Quit", shell.quit),
        ], align='l')
        contents = Column([
            title,
            menu,
        ], align = 'l', spacing=20)
        self.add_centered(contents)

    def screen_button(self, text: str, screen: Screen):
        return Button(text, action=lambda: self.shell.show_screen(screen))

    def quit(self):
        sys.exit(0)
