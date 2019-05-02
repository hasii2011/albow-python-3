

from albow.widgets.CheckBox import CheckBox

from albow.media.MusicUtilities import get_music_enabled
from albow.media.MusicUtilities import set_music_enabled

class EnableMusicControl(CheckBox):

    def get_value(self):
        return get_music_enabled()

    def set_value(self, newState: bool):
        set_music_enabled(newState)
