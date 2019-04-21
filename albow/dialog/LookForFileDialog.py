
import os

from albow.dialog.FileOpenDialog import FileOpenDialog


class LookForFileDialog(FileOpenDialog):

    target = None

    def __init__(self, target, **kwds):

        super().__init__(**kwds)
        self.target = target

    def item_is_choosable(self, path):
        return path and os.path.basename(path) == self.target

    def filter(self, name):
        return name and os.path.basename(name) == self.target
