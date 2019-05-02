

from albow.widgets.CheckBox import CheckBox

import albow.media.MusicUtilities

class EnableMusicControl(CheckBox):

    def get_value(self):
        return MusicUtilities.get_music_enabled()

    def set_value(self, x):
        MusicUtilities.set_music_enabled(x)
