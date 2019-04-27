
from albow.shell import Shell
from albow.screen import Screen
from albow.resource import get_font

from albow.layout.Column import Column

from albow.widgets.Label import Label
from albow.widgets.Button import Button

from albow.dialog.DialogUtilities import alert
from albow.dialog.DialogUtilities import ask

from albow.dialog.FileDialogUtilities import request_old_filename
from albow.dialog.FileDialogUtilities import request_new_filename
from albow.dialog.FileDialogUtilities import look_for_file_or_directory


class DemoDialogScreen(Screen):
    """
    Dialogs
    """

    def __init__(self, shell: Shell):

        #
        # Python 3 update
        #
        super().__init__(shell)
        menu = Column([
            Button("Ask a Question",             self.test_ask),
            Button("Request Old Filename",       self.test_old),
            Button("Request New Filename",       self.test_new),
            Button("Look for File or Directory", self.test_lookfor),
        ], align='l')
        contents = Column([
            Label("File Dialogs", font=get_font(18, "VeraBd.ttf")),
            menu,
            Button("Menu", action=shell.show_menu),
        ], align='l', spacing=30)
        self.add_centered(contents)

    def test_ask(self):
        response = ask("Do you like mustard and avocado ice cream?", ["Yes", "No", "Undecided"])
        alert("You chose %r." % response)

    def test_old(self):
        path = request_old_filename()
        if path:
            alert("You chose %r." % path)
        else:
            alert("Cancelled.")

    def test_new(self):
        path = request_new_filename(prompt="Save booty as:", filename="treasure", suffix=".dat")
        if path:
            alert("You chose %r." % path)
        else:
            alert("Cancelled.")

    def test_lookfor(self):
        path = look_for_file_or_directory(prompt="Please find 'Vera.ttf'", target="Vera.ttf")
        if path:
            alert("You chose %r." % path)
        else:
            alert("Cancelled.")
