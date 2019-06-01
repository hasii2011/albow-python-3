
from pygame import Rect

from albow.core.ResourceUtility import ResourceUtility

from albow.utils import overridable_property

from albow.core.ui.Widget import Widget

from albow.themes.ThemeProperty import ThemeProperty


class Image(Widget):
    """
    An Image is a widget that displays an image.
    """
    highlight_color = ThemeProperty('highlight_color')
    """
        The image highlight color
    """
    image = overridable_property('image')
    """
    The image to display.  The behaviour of this property can be customised by overriding the `get_image()` method.
    """
    highlighted = False
    """
        Indicates whether or not to highlight the image;  Default is _False_
    """

    def __init__(self, theImage = None, theRect: Rect = None, **kwds):
        """
        TODO  Do a unit test on this class

        Initializes the widget to display the given image. The initial size is determined by the image.

        Args:
            theImage:  Either a string that is the image name and can be found via the resource lookup methods
            or an actual image.  (TBD) - I don't like this and will change the API to only accept image names

            theRect:   The pygame rectangle to draw in

            **kwds:
        """
        super().__init__(theRect, **kwds)

        if theImage:
            if isinstance(theImage, str):
                theImage = ResourceUtility.get_image(theImage)
            w, h = theImage.get_size()
            d = 2 * self.margin
            self.size = w + d, h + d
            self._image = theImage
        else:
            self._image = None

    def get_image(self):
        """
        Called to get the value of the image property. By overriding this method, you can make the widget display
        an image from an outside source.

        Returns: The pygame image

        """
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
