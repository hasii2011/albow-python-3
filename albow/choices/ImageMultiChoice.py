
from pygame import Surface
from pygame import Rect

from albow.utils import blit_in_rect

from albow.choices.MultiChoice import MultiChoice


class ImageMultiChoice(MultiChoice):
    """
    ImageMultichoice is a Multichoice control that displays its values in the form of images.
    """
    highlight_style = 'fill'
    sel_color = (255, 192, 19)
    margin = 5

    def __init__(self, images, values, **kwds):
        """
        Initialises the control with the given images and corresponding values.

        Args:
            images:   The images we want displayed

            values: The values to return when the image is selected

            **kwds:
        """
        image0 = images[0]
        w, h = image0.get_size()
        d = 2 * self.predict(kwds, 'margin')
        cell_size = w + d, h + d
        #
        # Python 3 update
        #
        super().__init__(cell_size, values, **kwds)

        self.images = images

    def draw_item(self, surface: Surface, imageIndex: int, rect: Rect):

        image = self.images[imageIndex]
        blit_in_rect(surface, image, rect, self.align, self.margin)

    def draw_prehighlight(self, surf: Surface, theItemNumber: int, theRect: Rect):

        color = self.sel_color
        surf.fill(color, theRect)
