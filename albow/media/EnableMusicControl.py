
import logging

musicLogger = logging.getLogger(__name__)

from albow.core.root import schedule

from albow.widgets.CheckBox import CheckBox

from albow.media.PlayList import PlayList

try:
    from pygame.mixer import music
except ImportError:
    music = None
    musicLogger.error("* * * Music module not available * * *")


music_enabled: bool = True
current_music = None
current_playlist: PlayList = None

change_delay:       int = 2  # Delay between end of one item and starting the next (sec)
next_change_delay:  int = 0
fadeout_time:       int = 1  # Time over which to fade out music (sec)


def get_music_enabled():
    return music_enabled


def jog_music():
    """
    If no music is currently playing, start playing the next item
    from the current playlist.
    """
    if music_enabled and not music.get_busy():
        start_next_music()


def music_end():

    musicLogger.info("music_end")
    schedule(next_change_delay, jog_music)


def start_next_music():
    """
    Start playing the next item from the current playlist immediately.
    """

    musicLogger.info("start_music")
    global current_music, next_change_delay
    if music_enabled and current_playlist:
        next_music = current_playlist.next()
        if next_music:
            # print "albow.music: loading", repr(next_music) ###
            music.load(next_music)
            music.play()
            next_change_delay = change_delay
        current_music = next_music


def set_music_enabled(state:  bool):

    global music_enabled
    if music_enabled != state:
        music_enabled = state
        if state:
            # Music pausing doesn't always seem to work.
            # music.unpause()
            if current_music:
                # After stopping and restarting currently loaded music,
                # fadeout no longer works.
                # print "albow.music: reloading", repr(current_music) ###
                music.load(current_music)
                music.play()
            else:
                jog_music()
        else:
            # music.pause()
            music.stop()


def change_playlist(new_playlist: PlayList):
    """
    Fade out any currently playing music and start playing from the given
    playlist.
    """

    musicLogger.info("change_playlist")
    global current_music, current_playlist, next_change_delay
    if music and new_playlist is not current_playlist:
        current_playlist = new_playlist
        if music_enabled:
            music.fadeout(fadeout_time * 1000)
            next_change_delay = max(0, change_delay - fadeout_time)
            jog_music()
        else:
            current_music = None


def change_music(new_music, repeat=False):
    """
    Fade out any currently playing music and start playing the given
    music file
    """

    musicLogger.info("change_music")
    if music and new_music is not current_music:
        if new_music:
            new_playlist = PlayList([new_music], repeat=repeat)
        else:
            new_playlist = None
        change_playlist(new_playlist)


class EnableMusicControl(CheckBox):

    def get_value(self):
        return get_music_enabled()

    def set_value(self, x):
        set_music_enabled(x)
