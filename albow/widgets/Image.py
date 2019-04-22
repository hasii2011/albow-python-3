
from widget_file import Widget
from widget_file import overridable_property

from theme import ThemeProperty

class Image(Widget):
    #  image   Image to display

    highlight_color = ThemeProperty('highlight_color')
    image           = overridable_property('image')
    highlighted     = False

    def __init__(self, image=None, rect=None, **kwds):
        Widget.__init__(self, rect, **kwds)
        if image:
            # if isinstance(image, basestring):
            if isinstance(image, str):			# Python 3 update probably not necessary -- hasii
                image = resource.get_image(image)
            w, h = image.get_size()
            d = 2 * self.margin
            self.size = w + d, h + d
            self._image = image

    def get_image(self):
        return self._image

    def set_image(self, x):
        self._image = x

    def draw(self, surf):
        if self.highlighted:
            surf.fill(self.highlight_color)
        self.draw_image(surf, self.image)

    def draw_image(self, surf, image):
        frame = surf.get_rect()
        r = image.get_rect()
        r.center = frame.center
        surf.blit(image, r)

