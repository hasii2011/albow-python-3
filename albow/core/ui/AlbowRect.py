
import logging

from pygame import Rect

from albow.core.RectUtility import RectUtility

from albow.vectors import subtract
from albow.vectors import add


class AlbowRect:

    left = RectUtility.rect_property('left')
    right = RectUtility.rect_property('right')
    top = RectUtility.rect_property('top')
    bottom = RectUtility.rect_property('bottom')
    width = RectUtility.rect_property('width')
    height = RectUtility.rect_property('height')
    size = RectUtility.rect_property('size')
    topleft = RectUtility.rect_property('topleft')
    topright = RectUtility.rect_property('topright')
    bottomleft = RectUtility.rect_property('bottomleft')
    bottomright = RectUtility.rect_property('bottomright')
    midleft = RectUtility.rect_property('midleft')
    midright = RectUtility.rect_property('midright')
    midtop = RectUtility.rect_property('midtop')
    midbottom = RectUtility.rect_property('midbottom')
    center = RectUtility.rect_property('center')
    centerx = RectUtility.rect_property('centerx')
    centery = RectUtility.rect_property('centery')

    debug_resize = False

    def __init__(self, thePygameRect: Rect = None):

        self.logger = logging.getLogger(__name__)
        self.subwidgets = []
        self.parent = None
        self.anchor = 'lt'
        """
        A string specifying how this widget is to change in size and position when its parent widget changes size. The 
        letters 'l', 'r', 't' and 'b' are used to anchor the widget to the left, right, top or bottom sides of its 
        parent. Anchoring it to both left and right, or both top and bottom, causes the widget to stretch or shrink when 
        its parent changes in width or height.
        """

        if thePygameRect and not isinstance(thePygameRect, Rect):
            raise TypeError("AlbowRect rect not a pygame.Rect")

        self._rect = Rect(thePygameRect or (0, 0, 100, 100))

    def get_rect(self):
        return self._rect

    def set_rect(self, x):

        old_size = self._rect.size
        self._rect = Rect(x)
        self._resized(old_size[0], old_size[1])

    rect = property(get_rect, set_rect)
    """
    bounds in parent's coordinates
    """

    def _resized(self, old_width, old_height):
        """

        Args:
            old_width:
            old_height:
        """
        new_width, new_height = self._rect.size
        dw = new_width - old_width
        dh = new_height - old_height
        if dw or dh:
            self.resized(dw, dh)

    def resized(self, dw, dh):
        """
        Called when the widget changes size as a result of assigning to its width, height or size attributes,
        with (dw, dh) being the amount of the change. The default is to call parent_resized on each of its subwidgets.

        Args:
            dw:  width
            dh:  height
        """
        if self.debug_resize:
            self.logger.info(f"AlbowRect.resized: {self} by: ({dw}, {dh}) to {self.size}")
        for widget in self.subwidgets:
            widget.parent_resized(dw, dh)

    def parent_resized(self, dw, dh):
        """
        Called when the widget's parent changes size as a result of assigning to its width, height or size
        attributes, with (dw, dh) being the amount of the change. The default is to resize and/or reposition
        the widget according to its anchor attribute.

        Args:
            dw:  Width
            dh:  Height
        """
        debug_resize = self.debug_resize or self.parent.debug_resize

        if debug_resize:
            self.logger.info(f"AlbowRect.parent_resized {self}, by ({dw}, {dh})")

        left, top, width, height = self._rect
        move = False
        resize = False
        anchor = self.anchor

        if dw and 'r' in anchor:
            if 'l' in anchor:
                resize = True
                width += dw
            else:
                move = True
                left += dw
        if dh and 'b' in anchor:
            if 't' in anchor:
                resize = True
                height += dh
            else:
                move = True
                top += dh

        if resize:
            if debug_resize:
                self.logger.info(f"AlbowRect.parent_resized: changing rect to ({left}, {top}, {width}, {height})")
            self.rect = (left, top, width, height)
        elif move:
            if debug_resize:
                self.logger.info(f"AlbowRect.parent_resized: moving to (%{left},{top})")
            self._rect.topleft = (left, top)

    def global_to_local(self, p):
        """
        Converts the given coordinate pair from PyGame screen coordinates to the widget's local coordinate system.

        Args:
            p:  The global coordinates

        Returns:  The widget's local coordinates
        """
        return subtract(p, self.local_to_global_offset())

    def local_to_global(self, p):
        """
        Converts the given coordinate pair from the widget's local coordinate system to PyGame screen coordinates.

        Args:
            p: Widget local coordinates

        Returns: global coordinates
        """
        return add(p, self.local_to_global_offset())

    def local_to_global_offset(self):

        d = self.topleft
        parent = self.parent
        if parent:
            d = add(d, parent.local_to_global_offset())
        return d

    def get_global_rect(self):

        p = self.local_to_global_offset()
        pTuple = tuple(p)
        s = self.rect.size

        return Rect(pTuple, s)
