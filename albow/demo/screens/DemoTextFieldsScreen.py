
from albow.core.ui.Shell import Shell

from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.input.TextField import TextField

from albow.widgets.TextBox import TextBox
from albow.widgets.CheckBox import CheckBox

from albow.layout.Column import Column
from albow.layout.Row import Row

from albow.layout.Grid import Grid

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoTextFieldsScreen(BaseDemoScreen):
    """
    Text Field
    """
    nameField:   TextField
    raceField:   TextField
    resultLabel: Label
    textBox:     TextBox
    lineCtr:     int = 0

    def __init__(self, shell: Shell):
        """

        Args:
            shell:  Our parent shell
        """
        super().__init__(shell)

        contents = DemoTextFieldsScreen.makeContents(self.backButton)
        self.add_centered(contents)

    @classmethod
    def ok(cls):
        cls.resultLabel.text = "You are a %s called %s." % (cls.raceField.text, cls.nameField.text)

    @classmethod
    def appendText(cls):

        cls.lineCtr += 1
        line:     str = f"Line {cls.lineCtr}{TextBox.LINE_SEPARATOR}"
        oldLines: str = cls.textBox.getText()

        oldLines += line
        cls.textBox.setText(oldLines)

    @classmethod
    def insertText(cls):
        cls.lineCtr += 1
        line: str = f'Line {cls.lineCtr}'
        cls.textBox.insertText(theNewLine=line)

    @classmethod
    def clearText(cls):

        cls.textBox.clearText()
        cls.lineCtr = 0

    @classmethod
    def deleteText(cls):
        cls.textBox.deleteText(2)

    @classmethod
    def makeTextBoxTesterContainer(cls) -> Row:

        cls.textBox = TextBox(theNumberOfColumns=20, theNumberOfRows=10)

        checkBoxRow: Row = Row([CheckBox(), Label('Last Line Visible')])

        appendTextButton: Button = Button('Append', action=cls.appendText)
        insertTextButton: Button = Button('Insert', action=cls.insertText)
        deleteTextButton: Button = Button('Delete', action=cls.deleteText)
        clearTextButton:  Button = Button('Clear ', action=cls.clearText)

        contentAttrs = {
            "align": "l"
        }
        buttHolder:           Column = Column([appendTextButton, insertTextButton, deleteTextButton, clearTextButton], **contentAttrs)
        textBoxControlHolder: Column = Column([checkBoxRow,   buttHolder], **contentAttrs)

        container: Row = Row([cls.textBox, textBoxControlHolder])

        return container

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

        cls.resultLabel = Label("")
        cls.resultLabel.width = 400

        minMaxAttrs = {'min': 50, 'max': 240}
        minMaxField: TextField = TextField(**minMaxAttrs)
        minMaxField.type = int
        minMaxField.set_text("222")

        okBtn = Button("OK", action=cls.ok)

        tbTestContainer = cls.makeTextBoxTesterContainer()
        contentAttrs = {
            "align": "c"
        }

        if backButton is None:
            contents: Column = Column([fieldGrid, cls.resultLabel, okBtn, minMaxField, tbTestContainer], **contentAttrs)
        else:
            contents: Column = Column([fieldGrid, cls.resultLabel, okBtn, minMaxField, tbTestContainer, backButton], **contentAttrs)

        return contents
