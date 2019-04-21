
import os

from albow.dialog.DialogUtilities import ask
from albow.dialog.FileDialog import FileDialog

class FileSaveDialog(FileDialog):

    saving         = True
    default_prompt = "Save as:"
    ok_label       = "Save"

    def get_filename(self):
        return self.filename_box.value

    def set_filename(self, x):
        dsuf = self.suffixes[0]
        if x.endswith(dsuf):
            x = x[:-len(dsuf)]
        self.filename_box.value = x

    filename = property(get_filename, set_filename)

    def get_pathname(self):
        path = os.path.join(self.directory, self.filename_box.value)
        suffixes = self.suffixes
        if suffixes and not path.endswith(suffixes[0]):
            path = path + suffixes[0]
        return path

    pathname = property(get_pathname)

    def double_click_file(self, name):
        self.filename_box.value = name

    def ok(self):
        path = self.pathname
        if os.path.exists(path):
            answer = ask("Replace existing '%s'?" % os.path.basename(path))
            #
            # Python 3 update
            # if answer <> "OK":
            if answer != "OK":
                return
        FileDialog.ok(self)

    def update(self):
        FileDialog.update(self)

    def ok_enable(self):

        #
        # Python 3 update
        #
        # return self.filename_box.text <> ""
        return self.filename_box.text != ""

