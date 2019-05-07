"""
The resource module exports some utility functions for finding, loading and caching various types of
resources.  By default, resource files are looked for in a directory named _Resources_ alongside the
.py file of the program's main module.

.. TODO::
    But that can be changed by assigning to the `resource_dir` module variable.

Resource names are specified in a platform-independent manner using a series of pathname components. Specific
resource types are looked for by default in subdirectories of the resources directory as follows:


| Types   |      |            Location |
| ------- | ---- | ------------------: |
| Fonts   |      |   *resources*/fonts |
| Sounds  |      |  *resources*/sounds |
| Text    |      |    *resources*/text |
| Cursors |      | *resources*/cursors |
| Music   |      |   *resources*/music |


The subdirectory can in some cases be overridden using the `prefix` parameter to the relevant resource-loading
function.  Each type of resource has a cache. The first time a resource with a given name is requested, it is
loaded and placed in the cache.  Subsequent requests for the same name will return the cached object.


"""
import os
import sys
import logging

import pygame
from pygame.locals import RLEACCEL

from albow.core.DummySound import DummySound

DEFAULT_SOUND_DIRECTORY   = "sounds"
DEFAULT_CURSORS_DIRECTORY = "cursors"
DEFAULT_IMAGES_DIRECTORY  = "images"
DEFAULT_FONTS_DIRECTORY   = "fonts"
DEFAULT_TEXT_DIRECTORY    = "text"

optimize_images   = True
"""
If `True`, images loaded with `get_image()` will have `convert_alpha()` called on them by default. Defaults to `True`.
"""
run_length_encode = False

DEFAULT_RESOURCE_DIRECTORY_NAMES = ["Resources", "resources"]

image_cache  = {}
font_cache   = {}
sound_cache  = {}
text_cache   = {}
cursor_cache = {}

dummy_sound = DummySound()

ourLogger = logging.getLogger(__name__)


class ResourceUtility:
    """
    Static class housing shortcut methods to quickly access system resources like

    - sounds
    - cursors
    - fonts
    - images
    - resource directories

    .. Note::
        Make unit tests for sound and cursor APIs since they are not currently demo'ed
    """

    @staticmethod
    def find_resource_dir():

        directory = sys.path[0]

        while True:
            for name in DEFAULT_RESOURCE_DIRECTORY_NAMES:
                path = os.path.join(directory, name)
                if os.path.exists(path):
                    return path
            parent = os.path.dirname(directory)
            if parent == directory:
                raise SystemError("albow: Unable to find Resources directory")
            directory = parent

    @staticmethod
    def resource_exists(*names, **kwds) -> bool:
        """
        Returns true if a resource exists with the given pathname components.

        Args:
            *names:

            **kwds:

        Returns:  `True` if it does, else `False`

        """
        return os.path.exists(ResourceUtility._resource_path("", names, **kwds))

    @staticmethod
    def get_image(*names, **kwds):
        """
        Loads the specified image from the images directory or returns it from the cache.

        .. WARNING::
            For some of the options to work correctly, you must have initialized the PyGame screen before calling get_image().
        Args:
            *names:

            **kwds:

        Returns:

        """
        prefix = kwds.pop('prefix', "%s" % DEFAULT_IMAGES_DIRECTORY)
        path = ResourceUtility._resource_path(prefix, names)
        return ResourceUtility._get_image(path, **kwds)

    @staticmethod
    def get_font(size, *names, **kwds):
        """
        Loads the specified font or returns it from the cache.

        Args:
            size:   This size font to load

            *names:

            **kwds:

        Returns:    A pygame font

        """
        path = ResourceUtility._resource_path("%s" % DEFAULT_FONTS_DIRECTORY, names, **kwds)
        key = (path, size)
        font = font_cache.get(key)
        if not font:
            try:
                font = pygame.font.Font(path, size)
            #
            # Python 3 update
            #
            # except IOError, e:
            except IOError as e:
                raise e.__class__("%s: %s" % (e, path))
            font_cache[key] = font
        return font

    @staticmethod
    def get_text(*names, **kwds):
        """
        Loads the contents of a text file as a string or returns it from the cache. The file is opened in
        universal newlines mode.

        Args:
            *names:
            **kwds:

        Returns:

        """
        path = ResourceUtility._resource_path("%s" % DEFAULT_TEXT_DIRECTORY, names, **kwds)
        text = text_cache.get(path)
        if text is None:
            text = open(path, "rU").read()
            text_cache[path] = text
        return text

    @staticmethod
    def resource_path(*names, **kwds) -> str:
        """
        Constructs a resource pathname from the given pathname components.

        Args:
            *names:

            **kwds:

        Returns:    The resource path

        """
        return ResourceUtility._resource_path("", names, **kwds)

    @staticmethod
    def get_sound(*names, **kwds):
        """
        Loads the specified sound or returns it from the cache.

        If the sound is unable to be loaded for any reason, a warning message is printed and a dummy sound object
        with no-op methods is returned. This allows an application to continue without sound in an environment
        where sound support is not available.

        Args:
            *names:  Sound file name

            **kwds:

        Returns:

        """
        path = ResourceUtility._resource_path("%s" % DEFAULT_SOUND_DIRECTORY, names, **kwds)

        return ResourceUtility.load_sound(path)

    @staticmethod
    def load_sound(path) -> 'Sound':
        """
        Loads a sound from the file specified by path, or returns it from the cache. Like `get_sound()`,
        returns a dummy sound object if the sound cannot be loaded.
        
        Args:
            path:  Fully qualified path

        Returns: A pygame sound object

        """
        if sound_cache is None:
            return dummy_sound
        sound = sound_cache.get(path)
        if not sound:
            try:
                from pygame.mixer import Sound
            #
            # Python 3 update
            #
            # except ImportError, e:
            except ImportError as e:
                ResourceUtility.no_sound(e)
                return dummy_sound
            try:
                sound = Sound(path)
            #
            # Python 3 update
            #
            # except pygame.error, e:
            except pygame.error as e:
                ResourceUtility.missing_sound(e, path)
                return dummy_sound
            sound_cache[path] = sound

        return sound

    @staticmethod
    def no_sound(e):
        """
        Clear the sound cache as a side-effect

        :param e: Exception to log
        :return:
        """
        global sound_cache

        ourLogger.error("albow.resource.get_sound: %s", e)
        ourLogger.error("albow.resource.get_sound: Sound not available, continuing without it")

        sound_cache = None

    @staticmethod
    def missing_sound(e, name):
        """
        Log an error message on a missing sound

        :param e: The exception
        :param name: This name of the missing sound
        :return:
        """
        ourLogger.error("albow.resource.get_sound: %s: %s", name, e)

    @staticmethod
    def get_cursor(*names, **kwds):
        """
        Get a cursor out of the cache,  Else load it and cache it

        :param names:
        :param kwds:
        :return:
        """

        path = ResourceUtility._resource_path("%s" % DEFAULT_CURSORS_DIRECTORY, names, **kwds)
        cursor = cursor_cache.get(path)
        if cursor is None:
            cursor = ResourceUtility.load_cursor(path)
            cursor_cache[path] = cursor
        return cursor

    @staticmethod
    def load_cursor(path):
        """
        Loads a cursor from an image file or returns it from the cache. The cursor is returned as a tuple of
        arguments suitable for passing to the PyGame function `set_cursor()`.

        .. IMPORTANT::
            The image must be no larger than 16x16 pixels and should consist only of the colours black (0, 0, 0),
            white (255, 255, 255), blue (0, 0, 255) and cyan (0, 255, 255).  Blue and cyan are used to indicate the
            position of the hotspot, with blue if the hotspot is over a black or transparent pixel, and cyan if it is
            over a white pixel.  The hotspot defaults to the top left corner.  If the image has an alpha channel, it
            should consist of fully opaque or fully transparent pixels.

        Args:
            path:  A fully qualified path the the image file

        Returns:

        """
        image = ResourceUtility._get_image(path)
        width, height = image.get_size()
        hot = (0, 0)
        data = []
        mask = []
        rowbytes = (width + 7) // 8
        #
        # Python 3 update
        #
        # xr = xrange(width)
        # yr = xrange(height)
        xr = range(width)
        yr = range(height)

        for y in yr:
            bit = 0x80
            db = mb = 0
            for x in xr:
                r, g, b, a = image.get_at((x, y))
                if a >= 128:
                    mb |= bit
                    if r + g + b < 383:
                        db |= bit
                if r == 0 and b == 255:
                    hot = (x, y)
                bit >>= 1
                if not bit:
                    data.append(db)
                    mask.append(mb)
                    db = mb = 0
                    bit = 0x80
            # if bit <> 0x80:
            if bit != 0x80:
                data.append(db)
                mask.append(mb)
        return (8 * rowbytes, height), hot, data, mask

    @staticmethod
    def _resource_path(default_prefix, names, prefix="") -> str:

        return os.path.join(ResourceUtility.find_resource_dir(), prefix or default_prefix, *names)

    @staticmethod
    def _get_image(path, border=0, optimize=optimize_images, noalpha=False, rle=run_length_encode):
        """
        Loads the specified image from the images directory or returns it from the cache.

        Args:
            path:

            border: If border is specified, a border of that number of pixels is stripped from around the
            image (making it 2 * border pixels smaller in each direction).

            optimize: If optimize is true, convert_alpha() is called on the image.

            noalpha: If noalpha is true, any alpha channel is stripped from the image.

            rle:    If rle is true, the image is run-length encoded to improve blitting speed.

        Returns:  The specified image from the images directory or returns it from the cache
        """
        image = image_cache.get(path)
        if not image:
            image = pygame.image.load(path)
            if noalpha:
                image = image.convert(24)
            elif optimize:
                image = image.convert_alpha()
            if rle:
                image.set_alpha(255, RLEACCEL)
            if border:
                w, h = image.get_size()
                b = border
                d = 2 * border
                image = image.subsurface(b, b, w - d, h - d)
            image_cache[path] = image
        return image
