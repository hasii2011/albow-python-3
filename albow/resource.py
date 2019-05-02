import os
import sys

import pygame
from pygame.locals import RLEACCEL

optimize_images = True
run_length_encode = False

default_resource_dir_names = ["Resources", "resources"]


def find_resource_dir():

    directory = sys.path[0]
    while 1:
        for name in default_resource_dir_names:
            path = os.path.join(directory, name)
            if os.path.exists(path):
                return path
        parent = os.path.dirname(directory)
        if parent == directory:
            raise SystemError("albow: Unable to find Resources directory")
        directory = parent


resource_dir = find_resource_dir()

image_cache = {}
font_cache = {}
sound_cache = {}
text_cache = {}
cursor_cache = {}


def _resource_path(default_prefix, names, prefix="") -> str:
    return os.path.join(resource_dir, prefix or default_prefix, *names)


def resource_path(*names, **kwds) -> str:
    return _resource_path("", names, **kwds)


def resource_exists(*names, **kwds) -> bool:
    return os.path.exists(_resource_path("", names, **kwds))


def _get_image(path, border=0, optimize=optimize_images, noalpha=False, rle=run_length_encode):
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


def get_image(*names, **kwds):

    prefix = kwds.pop('prefix', "images")
    path = _resource_path(prefix, names)
    return _get_image(path, **kwds)


def get_font(size, *names, **kwds):
    path = _resource_path("fonts", names, **kwds)
    key = (path, size)
    font = font_cache.get(key)
    if not font:
        try:
            font = pygame.font.Font(path, size)
        # except IOError, e:
        except IOError as e:
            raise e.__class__("%s: %s" % (e, path))
        font_cache[key] = font
    return font


class DummySound:
    def fadeout(self, x): pass

    def get_length(self): return 0.0

    def get_num_channels(self): return 0

    def get_volume(self): return 0.0

    def play(self, *args): pass

    def set_volume(self, x): pass

    def stop(self): pass


dummy_sound = DummySound()


def load_sound(path):
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
            no_sound(e)
            return dummy_sound
        try:
            sound = Sound(path)
        #
        # Python 3 update
        #
        # except pygame.error, e:
        except pygame.error as e:
            missing_sound(e, path)
            return dummy_sound
        sound_cache[path] = sound
    return sound


def get_sound(*names, **kwds):
    path = _resource_path("sounds", names, **kwds)
    return load_sound(path)


def no_sound(e):
    global sound_cache
    print("albow.resource.get_sound: %s" % e)
    print("albow.resource.get_sound: Sound not available, continuing without it")
    sound_cache = None


def missing_sound(e, name):
    print("albow.resource.get_sound: %s: %s" % (name, e))


def get_text(*names, **kwds):
    path = _resource_path("text", names, **kwds)
    text = text_cache.get(path)
    if text is None:
        text = open(path, "rU").read()
        text_cache[path] = text
    return text


def load_cursor(path):
    image = _get_image(path)
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


def get_cursor(*names, **kwds):
    path = _resource_path("cursors", names, **kwds)
    cursor = cursor_cache.get(path)
    if cursor is None:
        cursor = load_cursor(path)
        cursor_cache[path] = cursor
    return cursor
