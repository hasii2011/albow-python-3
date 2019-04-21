
import os

from albow.dialog.FileDialog import FileDialog


class FileOpenDialog(FileDialog):

    saving = False
    ok_label = "Open"

    def get_pathname(self):
        name = self.list_box.get_selected_name()
        if name:
            return os.path.join(self.directory, name)
        else:
            return None

    pathname = property(get_pathname)

    def ok_enable(self):
        path = self.pathname
        enabled = self.item_is_choosable(path)
        return enabled

    def item_is_choosable(self, path):
        return bool(path) and self.filter(path)

    def double_click_file(self, name):
        self.ok()
