
from albow.core.ui.Shell import Shell

from albow.core.ResourceUtility import ResourceUtility

from albow.layout.Column import Column

from albow.widgets.Label import Label
from albow.widgets.Button import Button

from albow.dialog.TitledDialog import TitledDialog

from albow.dialog.DialogUtilities import alert
from albow.dialog.DialogUtilities import ask

from albow.dialog.FileDialogUtilities import request_old_filename
from albow.dialog.FileDialogUtilities import request_new_filename
from albow.dialog.FileDialogUtilities import look_for_file_or_directory

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoDialogScreen(BaseDemoScreen):
    """
    Dialogs
    """

    def __init__(self, shell: Shell):

        super().__init__(shell)

        contents = DemoDialogScreen.makeContents(self.backButton)
        self.add_centered(contents)

    @classmethod
    def makeContents(cls, backButton: Button = None) -> Column:

        menu = Column([
            Button(text="Ask a Question",      action=cls.test_ask),
            Button(text="Ask Old Filename",    action=cls.test_old),
            Button(text="Ask New Filename",    action=cls.test_new),
            Button(text="Look File/Directory", action=cls.test_lookfor),
            Button(text="Titled Dialog",       action=cls.testTitledDialog),
        ], align='l', expand=3, equalize='w')

        if backButton is None:
            contents = Column([
                menu,
            ], align='c', spacing=30)
        else:
            contents = Column([
                Label("File Dialogs", font=ResourceUtility.get_font(18, "VeraBd.ttf")),
                menu,
                backButton,
            ], align='c', spacing=30)

        return contents

    @classmethod
    def test_ask(cls):
        response = ask("Do you like mustard and avocado ice cream?", ["Yes", "No", "Undecided"])
        alert(f"You chose {response}.")

    @classmethod
    def test_old(cls):
        path = request_old_filename()
        if path:
            alert(f"You chose {path}.")
        else:
            alert("Cancelled.")

    @classmethod
    def test_new(cls):
        path = request_new_filename(prompt="Save booty as:", filename="treasure", suffix=".dat")
        if path:
            alert(f"You chose {path}.")
        else:
            alert("Cancelled.")

    @classmethod
    def test_lookfor(cls):
        path = look_for_file_or_directory(prompt="Please find 'Vera.ttf'", target="Vera.ttf")
        if path:
            alert(f"You chose {path}.")
        else:
            alert("Cancelled.")

    @classmethod
    def testTitledDialog(cls):

        longMsg: str = (
            f'[.. to disarm the people; that it was the best and most effectual way to enslave them.'
            f'  but that they should not do it openly, but weaken them, and let them sink gradually, '
            f' by totally disusing and neglecting the militia.  -- George Mason]'
        )

        ttlDlg = TitledDialog(title='Three Button', thirdButtTxt='Just Quit', message='Three buttons with custom text')
        response = ttlDlg.present()
        alert(f'You responded: {response}')

        ttlDlg: TitledDialog = TitledDialog(title='Long wrapped message', message=longMsg)
        response = ttlDlg.present()
        alert(f'You responded: {response}')

        ttlDlg = TitledDialog(title='Chip8 Python', message='Version 0.5, by Humberto A. Sanchez II')
        response = ttlDlg.present()
        alert(f'You responded: {response}')


