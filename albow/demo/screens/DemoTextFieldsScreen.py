
from albow.core.Shell import Shell

from albow.themes.Theme import Theme

from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.input.TextField import TextField

from albow.layout.Row import Row
from albow.layout.Column import Column
from albow.layout.Grid import Grid

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoTextFieldsScreen(BaseDemoScreen):
    """
    Text Field
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

        labelAttrs = {
            "bg_color": Theme.WHITE,
            "fg_color": Theme.BLACK
        }

        nameLabel: Label          = Label("Name: ", **labelAttrs)
        self.nameField: TextField = TextField(width=150)
        raceLabel: Label          = Label("Race: ", **labelAttrs)
        self.raceField: TextField = TextField(width=150)

        rows = [
            [nameLabel, self.nameField],
            [raceLabel, self.raceField]
        ]
        fieldGrid: Grid = Grid(rows)

        self.resultLabel = Label("", font=self.labelFont, **self.labelAttrs)
        self.resultLabel.width = 400

        okBtnAttrs = {
            'font': self.smallButtonFont
        }

        okBtn = Button("OK", action=self.ok, **okBtnAttrs)

        contentAttrs = {
            "align": "c"
        }

        contents: Column = Column([fieldGrid, self.resultLabel, okBtn, self.backButton], **contentAttrs)

        self.add_centered(contents)

    def ok(self):
        self.resultLabel.text = "You are a %s called %s." % (self.raceField.text, self.nameField.text)
