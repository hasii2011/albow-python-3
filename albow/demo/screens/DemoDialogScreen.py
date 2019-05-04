
from albow.core.Shell import Shell

from albow.core.ResourceUtility import ResourceUtility

from albow.layout.Column import Column

from albow.widgets.Label import Label
from albow.widgets.Button import Button

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

        #
        # Python 3 update
        #
        super().__init__(shell)
        buttAttrs = {
            "font": self.smallButtonFont
        }
        menu = Column([
            Button(text="Ask a Question",             action=self.test_ask,     **buttAttrs),
            Button(text="Request Old Filename",       action=self.test_old,     **buttAttrs),
            Button(text="Request New Filename",       action=self.test_new,     **buttAttrs),
            Button(text="Look for File or Directory", action=self.test_lookfor, **buttAttrs),
        ], align='l')
        contents = Column([
            Label("File Dialogs", font=ResourceUtility.get_font(18, "VeraBd.ttf"), **self.labelAttrs),
            menu,
            self.backButton,
        ], align='c', spacing=30)
        self.add_centered(contents)

    @staticmethod
    def test_ask():
        response = ask("Do you like mustard and avocado ice cream?", ["Yes", "No", "Undecided"])
        alert("You chose %r." % response)

    @staticmethod
    def test_old():
        path = request_old_filename()
        if path:
            alert("You chose %r." % path)
        else:
            alert("Cancelled.")

    @staticmethod
    def test_new():
        path = request_new_filename(prompt="Save booty as:", filename="treasure", suffix=".dat")
        if path:
            alert("You chose %r." % path)
        else:
            alert("Cancelled.")

    @staticmethod
    def test_lookfor():
        path = look_for_file_or_directory(prompt="Please find 'Vera.ttf'", target="Vera.ttf")
        if path:
            alert("You chose %r." % path)
        else:
            alert("Cancelled.")
