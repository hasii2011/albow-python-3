
from albow.core.ui.Shell import Shell

from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.input.TextField import TextField


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

        nameLabel: Label          = Label("Name: ")
        self.nameField: TextField = TextField(width=150)
        raceLabel: Label          = Label("Race: ")
        self.raceField: TextField = TextField(width=150)

        rows = [
            [nameLabel, self.nameField],
            [raceLabel, self.raceField]
        ]
        fieldGrid: Grid = Grid(rows)

        self.resultLabel = Label("", font=self.labelFont)
        self.resultLabel.width = 400

        minMaxAttrs = {'min': 50, 'max': 240}
        minMaxField: TextField = TextField(**minMaxAttrs)
        minMaxField.set_text("I should be 240 wide")

        okBtnAttrs = {
            'font': self.smallButtonFont
        }

        okBtn = Button("OK", action=self.ok, **okBtnAttrs)

        contentAttrs = {
            "align": "c"
        }

        contents: Column = Column([fieldGrid, self.resultLabel, okBtn, minMaxField, self.backButton], **contentAttrs)

        self.add_centered(contents)

    def ok(self):
        self.resultLabel.text = "You are a %s called %s." % (self.raceField.text, self.nameField.text)
