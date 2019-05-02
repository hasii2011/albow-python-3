
import os

from albow.resource import resource_path

from albow.media.PlayList import PlayList
from albow.media.MusicOptionsDialog import MusicOptionsDialog

try:
    from pygame.mixer import music
except ImportError:
    music = None
    print("Music not available")


# fadeout_time = 1  # Time over which to fade out music (sec)
# change_delay = 2  # Delay between end of one item and starting the next (sec)


# music_enabled = True
# current_music = None
# current_playlist = None
# next_change_delay = 0


def get_music(*names, **kwds):
    """
    Return the full pathname of a music file from the "music" resource
    subdirectory.
    """
    prefix = kwds.pop('prefix', "music")
    return resource_path(prefix, *names)


def get_playlist(*names, **kwds):
    prefix = kwds.pop('prefix', "music")
    dirpath = get_music(*names, **{'prefix': prefix})
    items = [os.path.join(dirpath, filename)
             for filename in os.listdir(dirpath)
             if not filename.startswith(".")]
    items.sort()
    return PlayList(items, **kwds)


# def change_playlist(new_playlist):
#     """
#     Fade out any currently playing music and start playing from the given
#     playlist.
#     """
#
#     # print "albow.music: change_playlist" ###
#     global current_music, current_playlist, next_change_delay
#     if music and new_playlist is not current_playlist:
#         current_playlist = new_playlist
#         if music_enabled:
#             music.fadeout(fadeout_time * 1000)
#             next_change_delay = max(0, change_delay - fadeout_time)
#             jog_music()
#         else:
#             current_music = None
#

# def change_music(new_music, repeat = False):
#     """Fade out any currently playing music and start playing the given
#     music file."""
#     #print "albow.music: change_music" ###
#     if music and new_music is not current_music:
#         if new_music:
#             new_playlist = PlayList([new_music], repeat = repeat)
#         else:
#             new_playlist = None
#         change_playlist(new_playlist)
#

# def music_end():
#     # print "albow.music: music_end" ###
#     schedule(next_change_delay, jog_music)


# def jog_music():
#     """If no music is currently playing, start playing the next item
#     from the current playlist."""
#     if music_enabled and not music.get_busy():
#         start_next_music()
#
#
# def start_next_music():
#     """Start playing the next item from the current playlist immediately."""
#     #print "albow.music: start_next_music" ###
#     global current_music, next_change_delay
#     if music_enabled and current_playlist:
#         next_music = current_playlist.next()
#         if next_music:
#             #print "albow.music: loading", repr(next_music) ###
#             music.load(next_music)
#             music.play()
#             next_change_delay = change_delay
#         current_music = next_music


# def get_music_enabled():
#     return music_enabled
#
#
# def set_music_enabled(state):
#     global music_enabled
#     if music_enabled != state:
#         music_enabled = state
#         if state:
#             # Music pausing doesn't always seem to work.
#             #music.unpause()
#             if current_music:
#                 # After stopping and restarting currently loaded music,
#                 # fadeout no longer works.
#                 #print "albow.music: reloading", repr(current_music) ###
#                 music.load(current_music)
#                 music.play()
#             else:
#                 jog_music()
#         else:
#             #music.pause()
#             music.stop()


def show_music_options_dialog():
    dlog = MusicOptionsDialog()
    dlog.present()
