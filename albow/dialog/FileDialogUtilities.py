#
#   Albow - File Dialogs
#

import os


from albow.dialog.FileDialog import FileDialog

from albow.dialog.DialogUtilities import ask



class FileSaveDialog(FileDialog):

    saving = True
    default_prompt = "Save as:"
    ok_label = "Save"

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
        # return self.filename_box.text <> ""
        return self.filename_box.text != ""


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

    #def update(self):
    #	FileDialog.update(self)

    def ok_enable(self):
        path = self.pathname
        enabled = self.item_is_choosable(path)
        return enabled

    def item_is_choosable(self, path):
        return bool(path) and self.filter(path)

    def double_click_file(self, name):
        self.ok()


class LookForFileDialog(FileOpenDialog):

    target = None

    def __init__(self, target, **kwds):
        FileOpenDialog.__init__(self, **kwds)
        self.target = target

    def item_is_choosable(self, path):
        return path and os.path.basename(path) == self.target

    def filter(self, name):
        return name and os.path.basename(name) == self.target


def request_new_filename(prompt=None, suffix=None, extra_suffixes=None, directory=None, filename=None, pathname=None):
    if pathname:
        directory, filename = os.path.split(pathname)
    if extra_suffixes:
        suffixes = extra_suffixes
    else:
        suffixes = []
    if suffix:
        suffixes = [suffix] + suffixes
    dlog = FileSaveDialog(prompt=prompt, suffixes=suffixes)
    if directory:
        dlog.directory = directory
    if filename:
        dlog.filename = filename
    if dlog.present():
        return dlog.pathname
    else:
        return None


def request_old_filename(suffixes=None, directory=None):
    """

    :param suffixes:
    :param directory:
    :return:
    """
    attrs = {'margin': 10}

    dlog = FileOpenDialog(suffixes=suffixes, **attrs)
    if directory:
        dlog.directory = directory
    if dlog.present():
        return dlog.pathname
    else:
        return None


def look_for_file_or_directory(target, prompt=None, directory=None):

    dlog = LookForFileDialog(target=target, prompt=prompt)
    if directory:
        dlog.directory = directory
    if dlog.present():
        return dlog.pathname
    else:
        return None
