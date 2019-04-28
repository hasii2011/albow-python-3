
from albow.core.screen import Screen
from albow.resource import get_font

from albow.widgets.Label import Label
from albow.widgets.Button import Button

from albow.layout.Column import Column

from albow.themes.Theme import Theme

from albow.demo.views.DemoTableView import DemoTableView


class DemoTableScreen(Screen):
    """
    Table View
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

        f        = get_font(15, "VeraBd.ttf")
        title    = Label("Norwegian Butter Exports", font=f)
        #
        # Python 3/pygame 1.9 update
        #
        attrs = {
            'fg_color':     Theme.WHITE,
            'border_color': Theme.BLACK,
            'sel_color':    (255, 196, 13),
            'bg_color':     (45, 137, 239)
        }
        table    = DemoTableView(**attrs)
        back     = Button("Back to Menu", action=shell.show_menu)
        contents = Column([title, table, back], spacing=30)

        self.add_centered(contents)
