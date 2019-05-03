
from albow.core.Shell import Shell

from albow.layout.Column import Column

from albow.widgets.Label import Label

from albow.demo.views.DemoPaletteView import DemoPaletteView

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoPaletteViewScreen(BaseDemoScreen):

    def __init__(self, shell: Shell):

        #
        # Python 3 update
        #
        super().__init__(shell)

        w, h = self.size        # Extract from tuple

        grid = DemoPaletteView()
        lbl  = Label("Cl1ck a Squ4r3", **self.labelAttrs)

        grid.border_width = 1
        grid.center = (w/2, h/2)
        grid.output = lbl
        columnAttrs = {
            "align": "c",
            'expand': 0
        }

        contents = Column([grid, lbl, self.backButton], **columnAttrs)
        self.add_centered(contents)

    def go_back(self):
        self.parent.show_menu()
