
from pygame import Surface

import logging

from albow.core.ResourceUtility import ResourceUtility

from albow.utils import overridable_property

from albow.widgets.ButtonBase import ButtonBase

from albow.widgets.Image import Image


class ImageButton(ButtonBase, Image):
    """

    An ImageButton is a button whose appearance is defined by an image.
    """
    disabledBgImage = overridable_property('disabledBgImage')
    """
        This disabled background image
    """
    enabledBgImage = overridable_property('enabledBgImage')
    """
    The enabled background image
    """
    highlightedBgImage = overridable_property('highlightedBgImage')
    """
        The highlighted background image
    """
    def __init__(self, disabledBgImage: str = None, enabledBgImage: str = None, highlightedBgImage: str = None, **kwds):
        """
        You must as a minimum supply a single image via `theImage` parameter.  Optionally, you can supply
        enabled, disabled, and highlighted images

        Args:
            disabledBgImage:  The image to display when the button is disabled

            enabledBGImage:  The image to display when the button is enabled

            highlightedBgImage: The image to display when the button is highlighted

            **kwds:
        """
        Image.__init__(self, **kwds)

        self.logger = logging.getLogger(__name__)
        self._disabledBgImage = None
        self._enabledBgImage = None
        self._highlightedBgImage = None

        if disabledBgImage != None:
            self._disabledBgImage = ResourceUtility.get_image(disabledBgImage)

        if enabledBgImage != None:
            self._enabledBgImage = ResourceUtility.get_image(enabledBgImage)

        if highlightedBgImage != None:
            self._highlightedBgImage = ResourceUtility.get_image(highlightedBgImage)

    def get_disabledBgImage(self):
        return self._disabledBgImage

    def set_disabledBgImage(self, theNewImage: Surface):
        self._disabledBgImage = theNewImage

    def get_enabledBgImage(self):
        return self._enabledBgImage

    def set_enabledBgImage(self, theNewImage: Surface):
        self._enabledBgImage = theNewImage

    def get_highlightedBgImage(self) -> Surface:
        return self._highlightedBgImage

    def set_highlightedBgImage(self, theNewImage: Surface):
        self._highlightedBgImage = theNewImage

    def get_highlighted(self):
        return self._highlighted

    def set_highlighted(self, theNewValue: bool):
        self._highlighted = theNewValue

    def draw(self, surface: Surface):

        dbi = self.disabledBgImage
        ebi = self.enabledBgImage
        hbi = self.highlightedBgImage

        if not self.enabled:
            if dbi:
                self.draw_image(surface, dbi)
        elif self.highlighted:
            if hbi:
                self.draw_image(surface, hbi)
            else:
                surface.fill(self.highlight_color)
        else:
            if ebi:
                self.draw_image(surface, ebi)
        fgi = self.image
        if fgi:
            self.draw_image(surface, fgi)
