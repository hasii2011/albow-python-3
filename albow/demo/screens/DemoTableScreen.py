
from albow.widgets.Label import Label

from albow.layout.Column import Column

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
        super().__init__(shell)

        title = Label("Norwegian Butter Exports", font=self.labelFont)
        table: DemoTableView = DemoTableView()

        contents = Column([title, table, self.backButton], spacing=BaseDemoScreen.DEFAULT_CONTENT_SPACING)

        self.add_centered(contents)
