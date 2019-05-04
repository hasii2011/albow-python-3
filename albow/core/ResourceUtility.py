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
run_length_encode = False

default_resource_dir_names = ["Resources", "resources"]

image_cache  = {}
font_cache   = {}
sound_cache  = {}
text_cache   = {}
cursor_cache = {}

dummy_sound = DummySound()

ourLogger = logging.getLogger(__name__)


class ResourceUtility:
    """
    Static class housing shortcut methods to quickly access

    system resources like
        sounds
        cursors
        fonts
        images
        resource directories

    TODO  Make unit tests for sound and cursor APIs since they are not currently demo'ed
    """

    @staticmethod
    def find_resource_dir():

        directory = sys.path[0]

        while True:
            for name in default_resource_dir_names:
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

        :param names:
        :param kwds:
        :return: True if it does, else False
        """
        return os.path.exists(ResourceUtility._resource_path("", names, **kwds))

    @staticmethod
    def get_image(*names, **kwds):
        """

        :param names:
        :param kwds:
        :return:
        """

        prefix = kwds.pop('prefix', "%s" % DEFAULT_IMAGES_DIRECTORY)
        path = ResourceUtility._resource_path(prefix, names)
        return ResourceUtility._get_image(path, **kwds)

    @staticmethod
    def get_font(size, *names, **kwds):
        """

        :param size:
        :param names:
        :param kwds:
        :return:
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

        :param names:
        :param kwds:
        :return:
        """
        path = ResourceUtility._resource_path("%s" % DEFAULT_TEXT_DIRECTORY, names, **kwds)
        text = text_cache.get(path)
        if text is None:
            text = open(path, "rU").read()
            text_cache[path] = text
        return text

    @staticmethod
    def resource_path(*names, **kwds) -> str:
        return ResourceUtility._resource_path("", names, **kwds)

    @staticmethod
    def get_sound(*names, **kwds):
        """
        Load a sound

        :param names:
        :param kwds:
        :return:  a pygame sound resource
        """
        path = ResourceUtility._resource_path("%s" % DEFAULT_SOUND_DIRECTORY, names, **kwds)

        return ResourceUtility.load_sound(path)

    @staticmethod
    def load_sound(path):
        """
        Load a sound
        :param path:   The path where presumably the sound file exists

        :return:  A pygame sound resource
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

        :param path:
        :return:
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
        """

        :param default_prefix:
        :param names:
        :param prefix:
        :return:
        """
        return os.path.join(ResourceUtility.find_resource_dir(), prefix or default_prefix, *names)

    @staticmethod
    def _get_image(path, border=0, optimize=optimize_images, noalpha=False, rle=run_length_encode):
        """

        :param border:
        :param optimize:
        :param noalpha:
        :param rle:
        :return:
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
