
from albow.core.Screen import Screen
from albow.core.Shell import Shell

from albow.widgets.Label import Label
from albow.widgets.Button import Button

from albow.layout.Column import Column

from albow.demo.views.DemoGridView import DemoGridView


class DemoGridViewScreen(Screen):

    def __init__(self, shell: Shell):

        #
        # Python 3 update
        #
        super().__init__(shell)

        grid        = DemoGridView()
        lbl         = Label("Cl1ck a Squ4r3")
        grid.output = lbl
        btn         = Button("Menu", action=self.go_back)
        contents    = Column([grid, lbl, btn], align='l', spacing=30)
        self.add_centered(contents)

    def go_back(self):
        self.parent.show_menu()
