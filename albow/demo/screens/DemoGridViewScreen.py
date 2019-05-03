
from albow.core.Shell import Shell

from albow.widgets.Label import Label

from albow.layout.Column import Column

from albow.demo.views.DemoGridView import DemoGridView

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoGridViewScreen(BaseDemoScreen):

    def __init__(self, shell: Shell):

        #
        # Python 3 update
        #
        super().__init__(shell)

        grid        = DemoGridView()
        lbl         = Label("Cl1ck a Squ4r3")
        grid.output = lbl
        contents    = Column([grid, lbl, self.backButton],
                             align='c', spacing=30)
        self.add_centered(contents)
