
from albow.layout.Column import Column
from albow.layout.Grid import Grid

from albow.dialog.Dialog import Dialog
from albow.widgets.Label import Label
from albow.widgets.Button import Button

from albow.media.EnableMusicControl import EnableMusicControl
from albow.media.MusicVolumeControl import MusicVolumeControl


class MusicOptionsDialog(Dialog):
    """
    A simple dialog for controlling music-playing options. Incorporates an
    `albow.media.EnableMusicControl` and an `albow.media.MusicVolumeControl`.
    """
    def __init__(self):

        #
        # Python 3 update
        #
        super().__init__()
        emc = EnableMusicControl()
        mvc = MusicVolumeControl()
        controls = Grid([
            [Label("Enable Music"), emc],
            [Label("Music Volume"), mvc],
        ])
        buttons = Button("OK", self.ok)
        contents = Column([controls, buttons], align='r', spacing=20)
        contents.topleft = (20, 20)
        self.add(contents)
        self.shrink_wrap()

    def ok(self):
        self.dismiss(True)