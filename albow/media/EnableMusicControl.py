
from albow.widgets.CheckBox import CheckBox

from albow.media.MusicUtilities import MusicUtilities


class EnableMusicControl(CheckBox):
    """
    A control for enabling and disabling the playing of music by the `albow.media.MusicUtilities` module.
    """
    def get_value(self):
        return MusicUtilities.get_music_enabled()

    def set_value(self, newState: bool):
        MusicUtilities.set_music_enabled(newState)
