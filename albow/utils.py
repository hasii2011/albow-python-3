
import sys

from pygame import Surface
from pygame import Rect


# from pygame.locals import SRCALPHA


def overridable_property(name: str, doc:str =None):
    """
    Creates a property which calls methods _get_xxx_ and _set_xxx_ of
    the underlying object to get and set the property value, so that
    the property's behaviour may be easily overridden by subclasses.

    Args:
        name:  The property name
        doc:   The documentation associated with it

    Returns:  The property

    """
    getter_name = sys.intern('get_' + name)
    setter_name = sys.intern('set_' + name)
    return property(
        lambda self: getattr(self, getter_name)(),
        lambda self, value: getattr(self, setter_name)(value),
        None,
        doc)


def frame_rect(surface: Surface, color, rect: Rect, thick: int = 1):
    """
    Draws a border with thickness thick just inside the specified rectangle.

    Args:
        surface: Pygame surface

        color:
        rect: pygame rectangle

        thick:
    """
    surface.fill(color, (rect.left, rect.top, rect.width, thick))
    surface.fill(color, (rect.left, rect.bottom - thick, rect.width, thick))
    surface.fill(color, (rect.left, rect.top, thick, rect.height))
    surface.fill(color, (rect.right - thick, rect.top, thick, rect.height))


#
# This method is not used;  Also, use old & outdated
# Numeric module;  I am commenting it out with plans
# ot remove it
#
# def blit_tinted(surface, image, pos, tint, src_rect = None):
#
# 	from Numeric import array, add, minimum
# 	from pygame.surfarray import array3d, pixels3d
#
# 	if src_rect:
# 		image = image.subsurface(src_rect)
# 	buf = Surface(image.get_size(), SRCALPHA, 32)
# 	buf.blit(image, (0, 0))
# 	src_rgb = array3d(image)
# 	buf_rgb = pixels3d(buf)
# 	buf_rgb[...] = minimum(255, add(tint, src_rgb)).astype('b')
# 	buf_rgb = None
# 	surface.blit(buf, pos)


def blit_in_rect(dst, src, frame, align='tl', margin=0):
    """
    Draws the image onto the surface within the rectangle frame, aligned according to align. The
    alignment string may contain any meaningful combination of the letters

    - _l_
    - _r_
    - _t_
    - _b_
    - _c_

    for _left_, _right_, _top_, _bottom_ and _center_.

    For example, _bl_ aligns the bottom left corners of the image and frame, and _cr_
    aligns their center right points.  If a margin is specified, the frame is considered to be reduced in size by
    that amount on all sides.

    Args:
        dst:  destination

        src:	source

        frame:	frame

        align:	alignment string

        margin: margin to provide
    """
    r = src.get_rect()
    align_rect(r, frame, align, margin)
    dst.blit(src, r)


def align_rect(r, frame, align='tl', margin=0):
    """
    Modifies the rectangle rect so that it is aligned with the rectangle frame according to align
    and margin. See `blit_in_rect`.

    Args:
        r:
        frame:
        align:
        margin:
    """
    if 'l' in align:
        r.left = frame.left + margin
    elif 'r' in align:
        r.right = frame.right - margin
    else:
        r.centerx = frame.centerx
    if 't' in align:
        r.top = frame.top + margin
    elif 'b' in align:
        r.bottom = frame.bottom - margin
    else:
        r.centery = frame.centery


def brighten(rgb, factor):
    """
    Returns a new color obtained by multiplying each component of the color rgb by the given factor, which
    should be a number in the range 0.0 to 1.0.

    Args:
        rgb:	The color to brighten

        factor:	Should be a number in the range 0.0 to 1.0.

    Returns:
        A new RGB value
    """
    return [min(255, int(round(factor * c))) for c in rgb]
