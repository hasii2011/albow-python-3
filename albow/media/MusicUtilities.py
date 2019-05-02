
import os

from albow.resource import resource_path

from albow.media.PlayList import PlayList
from albow.media.MusicOptionsDialog import MusicOptionsDialog

try:
    from pygame.mixer import music
except ImportError:
    music = None
    print("Music not available")


def get_music(*names, **kwds) -> str:
    """
    Return the full pathname of a music file from the "music" resource subdirectory.
    """
    prefix = kwds.pop('prefix', "music")
    return resource_path(prefix, *names)


def get_playlist(*names, **kwds) -> PlayList:

    prefix = kwds.pop('prefix', "music")

    directoryPath = get_music(*names, **{'prefix': prefix})
    items = [os.path.join(directoryPath, filename)

             for filename in os.listdir(directoryPath)
             if not filename.startswith(".")]

    items.sort()

    return PlayList(items, **kwds)


def show_music_options_dialog():
    dlog = MusicOptionsDialog()
    dlog.present()
