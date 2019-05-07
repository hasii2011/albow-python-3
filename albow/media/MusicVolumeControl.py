
from pygame import Rect
from pygame import Surface

from pygame.event import Event

from albow.core.Widget import Widget

try:
    from pygame.mixer import music
except ImportError:
    music = None
    print("Music not available")

if music:
    #
    #  Pygame 1.9 update
    #  music.set_endevent(MUSIC_END_EVENT)
    #  This needs updating
    music.set_endevent()


class MusicVolumeControl(Widget):
    """
    A control for adjusting the volume of music played by the music module.
    """
    def __init__(self, **kwds):
        #
        # Python 3 update
        #
        super().__init__(Rect((0, 0), (100, 20)), **kwds)

    def draw(self, surf: Surface):

        r = self.get_margin_rect()
        r.width = int(round(music.get_volume() * r.width))
        surf.fill(self.fg_color, r)

    def mouse_down(self, e: Event):
        self.mouse_drag(e)

    def mouse_drag(self, e: Event):

        m = self.margin
        w = self.width - 2 * m
        x = max(0.0, min(1.0, (e.local[0] - m) / w))
        music.set_volume(x)
        self.invalidate()
