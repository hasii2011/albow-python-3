
from albow.core.Screen import Screen
from albow.core.shell import Shell

from albow.widgets.Button import Button

from albow.demo.views.DemoPaletteView import DemoPaletteView


class DemoPaletteViewScreen(Screen):

    def __init__(self, shell: Shell):

        #
        # Python 3 update
        #
        super().__init__(shell)

        w, h = self.size        # Extract from tuple

        grid = DemoPaletteView()
        grid.center = (w/2, h/2)
        self.add(grid)

        btn = Button("Menu", action=self.go_back)
        btn.center = (w/2, h - 50)

        self.add(btn)

    def go_back(self):
        self.parent.show_menu()
