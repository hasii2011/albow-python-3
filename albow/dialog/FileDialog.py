
import os

from albow.themes.ThemeProperty import ThemeProperty

from albow.dialog.Dialog import Dialog
from albow.dialog.DirectoryPathView import DirectoryPathView
from albow.dialog.FileListView import FileListView

from albow.widgets.Label import Label
from albow.widgets.Button import Button

from albow.layout.Row import Row
from albow.layout.Column import Column
from albow.input.TextField import TextField


class FileDialog(Dialog):

    box_width = 250
    default_prompt = None
    up_button_text = ThemeProperty("up_button_text")

    def __init__(self, prompt=None, suffixes=None, **kwds):

        super().__init__(**kwds)

        label         = None
        d             = self.margin
        self.suffixes = suffixes or ()
        up_button     = Button(self.up_button_text, action=self.go_up)
        dir_box       = DirectoryPathView(self.box_width - up_button.width - 10, self)
        self.dir_box  = dir_box
        top_row       = Row([dir_box, up_button])
        list_box      = FileListView(self.box_width - 16, self)
        self.list_box = list_box
        ctrls         = [top_row, list_box]
        prompt         = prompt or self.default_prompt

        if prompt:
            label = Label(prompt)
        if self.saving:
            filename_box = TextField(self.box_width)
            filename_box.change_action = self.update
            self.filename_box = filename_box
            ctrls.append(Column([label, filename_box], align='l', spacing=0))
        else:
            if label:
                ctrls.insert(0, label)

        ok_button      = Button(self.ok_label, action=self.ok, enable=self.ok_enable)
        self.ok_button = ok_button
        cancel_button  = Button("Cancel", action=self.cancel)
        vbox           = Column(ctrls, align='l', spacing=d)
        vbox.topleft   = (d, d)
        y              = vbox.bottom + d
        ok_button.topleft = (vbox.left, y)
        cancel_button.topright = (vbox.right, y)
        self.add(vbox)
        self.add(ok_button)
        self.add(cancel_button)
        self.shrink_wrap()
        self._directory = None
        self.directory = os.getcwd()
        # print "FileDialog: cwd =", repr(self.directory) ###
        if self.saving:
            filename_box.focus()

    def get_directory(self):
        return self._directory

    def set_directory(self, x):
        x = os.path.abspath(x)
        while not os.path.exists(x):
            y = os.path.dirname(x)
            if y == x:
                x = os.getcwd()
                break
            x = y
        # if self._directory <> x:
        if self._directory != x:
            self._directory = x
            self.list_box.update()
            self.update()

    directory = property(get_directory, set_directory)

    def filter(self, path):
        suffixes = self.suffixes
        if not suffixes:
            return os.path.isfile(path)
        for suffix in suffixes:
            if path.endswith(suffix):
                return True

    def update(self):
        pass

    def go_up(self):
        self.directory = os.path.dirname(self.directory)

    def dir_box_click(self, double):
        if double:
            name = self.list_box.get_selected_name()
            path = os.path.join(self.directory, name)
            suffix = os.path.splitext(name)[1]
            if suffix not in self.suffixes and os.path.isdir(path):
                self.directory = path
            else:
                self.double_click_file(name)
        self.update()

    def ok(self):
        self.dismiss(True)

    def cancel(self):
        self.dismiss(False)

