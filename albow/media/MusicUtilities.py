
import os

import logging

from albow.core.root import schedule

from albow.core.Res import resource_path

from albow.media.PlayList import PlayList

musicLogger = logging.getLogger(__name__)

try:
    from pygame.mixer import music
except ImportError:
    music = None
    musicLogger.error("Music not available")


music_enabled: bool = True
current_music       = None
current_playlist: PlayList = None

change_delay:       int = 2  # Delay between end of one item and starting the next (sec)
next_change_delay:  int = 0
fadeout_time:       int = 1  # Time over which to fade out music (sec)


class MusicUtilities:

    @staticmethod
    def jog_music():
        """
        If no music is currently playing, start playing the next item
        from the current playlist.
        """
        if music_enabled and not music.get_busy():
            MusicUtilities.start_next_music()

    @staticmethod
    def get_music_enabled():
        return music_enabled

    @staticmethod
    def set_music_enabled(state: bool):

        global music_enabled
        if music_enabled != state:
            music_enabled = state
            if state:
                if current_music:
                    # After stopping and restarting currently loaded music,
                    # fadeout no longer works.
                    # print "albow.music: reloading", repr(current_music) ###
                    music.load(current_music)
                    music.play()
                else:
                    MusicUtilities.jog_music()
            else:
                music.stop()

    @staticmethod
    def get_current_playlist() -> PlayList:
        return current_playlist

    @staticmethod
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
                MusicUtilities.jog_music()
            else:
                current_music = None

    @staticmethod
    def get_music(*names, **kwds) -> str:
        """
        Return the full pathname of a music file from the "music" resource subdirectory.
        """
        prefix = kwds.pop('prefix', "music")
        return resource_path(prefix, *names)

    @staticmethod
    def start_next_music():
        """
        Start playing the next item from the current playlist immediately.
        """

        musicLogger.info("start_next_music")
        global current_music, next_change_delay
        if music_enabled and current_playlist:
            next_music = current_playlist.next()
            if next_music:
                musicLogger.info("albow.music: loading %s", repr(next_music))
                music.load(next_music)
                music.play()
                next_change_delay = change_delay
            current_music = next_music

    @staticmethod
    def get_playlist(*names, **kwds) -> PlayList:

        prefix = kwds.pop('prefix', "music")

        directoryPath = MusicUtilities.get_music(*names, **{'prefix': prefix})
        items = [os.path.join(directoryPath, filename)

                 for filename in os.listdir(directoryPath)
                 if not filename.startswith(".")]

        items.sort()

        return PlayList(items, **kwds)

    @staticmethod
    def music_end():

        musicLogger.info("music_end")
        schedule(next_change_delay, MusicUtilities.jog_music)

    @staticmethod
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
            MusicUtilities.change_playlist(new_playlist)

