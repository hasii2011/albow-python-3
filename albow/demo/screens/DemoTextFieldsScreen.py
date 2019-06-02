
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
    nameField: TextField
    raceField: TextField
    resultLabel: Label

    def __init__(self, shell: Shell):
        """

        :param shell:
        """
        super().__init__(shell)

        contents = DemoTextFieldsScreen.makeContents(self.backButton)
        self.add_centered(contents)

    @classmethod
    def ok(cls):
        cls.resultLabel.text = "You are a %s called %s." % (cls.raceField.text, cls.nameField.text)

    @classmethod
    def makeContents(cls, backButton: Button = None) -> Column:

        nameLabel: Label = Label("Name: ")
        raceLabel: Label = Label("Race: ")

        cls.nameField: TextField = TextField(width=150)
        cls.raceField: TextField = TextField(width=150)

        rows = [
            [nameLabel, cls.nameField],
            [raceLabel, cls.raceField]
        ]
        fieldGrid: Grid = Grid(rows)

        # cls.resultLabel = Label("", font=self.labelFont)
        cls.resultLabel = Label("")
        cls.resultLabel.width = 400

        minMaxAttrs = {'min': 50, 'max': 240}
        minMaxField: TextField = TextField(**minMaxAttrs)
        minMaxField.set_text("I should be 240 wide")

        okBtn = Button("OK", action=cls.ok)

        contentAttrs = {
            "align": "c"
        }

        if backButton is None:
            contents: Column = Column([fieldGrid, cls.resultLabel, okBtn, minMaxField], **contentAttrs)
        else:
            contents: Column = Column([fieldGrid, cls.resultLabel, okBtn, minMaxField, backButton], **contentAttrs)

        return contents
