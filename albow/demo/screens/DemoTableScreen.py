
from albow.widgets.Label import Label

from albow.layout.Column import Column

from albow.themes.Theme import Theme

from albow.demo.views.DemoTableView import DemoTableView

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoTableScreen(BaseDemoScreen):
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

        title    = Label("Norwegian Butter Exports", font=self.labelFont, **self.labelAttrs)
        #
        # Python 3/pygame 1.9 update
        #
        attrs = {
            'fg_color':            Theme.WHITE,
            'border_color':        Theme.BLACK,
            'sel_color':           (208,210,211),
            'bg_color':            (24,189,207),
            'header_bg_color':     Theme.BLACK
        }
        table: DemoTableView = DemoTableView(**attrs)

        contents = Column([title, table, self.backButton], spacing=30)

        self.add_centered(contents)
