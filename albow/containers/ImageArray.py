
from pygame import Rect
from pygame import Surface

from albow.core.ResourceUtility import ResourceUtility


class ImageArray:
    """
    An ImageArray is an indexed collection of images created by dividing up a master image into equal-sized subimages.

    Image arrays can be one-dimensional or two-dimensional. A one-dimensional image array has its
    subimages arranged horizontally in the master image and is indexed by an integer. A two-dimensional image array is
    indexed by a ``tuple (row, col)``.

    """
    ncols = 0
    nrows = 0
    size  = (0,0)

    def __init__(self, image, shape):
        """
        Constructs an image array from the given image, which should be a Surface.

        Args:
            image:  The surface that is the image

            shape:  The shape is either an  integer for a one-dimensional image array,
            or a tuple (num_rows, num_cols) for a two-dimensional image array.
        """
        self.image = image
        self.shape = shape
        if isinstance(shape, tuple):
            self.nrows, self.ncols = shape
        else:
            #self.nrows = 1
            self.nrows = None
            self.ncols = shape
        iwidth, iheight = image.get_size()
        self.size = iwidth // self.ncols, iheight // (self.nrows or 1)

    def __len__(self):
        """
        Returns the shape of the image array (an integer if one-dimensional, or a 2-tuple if two-dimensional).

        Returns:  The shape

        """
        result = self.shape
        if isinstance(result, tuple):
            raise TypeError("Can only use len() on 1-dimensional image array")
        return result

    def __nonzero__(self):
        return True

    def __getitem__(self, theIndex):
        """
        Returns a subsurface for the image at index theIndex of a one-dimensional image array.

        Args:
            theIndex: The index of the image to return

        Returns:

        """
        image = self.image
        nrows = self.nrows
        ncols = self.ncols
        if nrows is None:
            row = 0
            col = theIndex
        else:
            row, col = theIndex
        width, height = self.size
        left = width * col
        top = height * row
        return image.subsurface(left, top, width, height)

    def get_rect(self) -> Rect:
        """
        Creates and returns a bounding rectangle for one of the subimages, with top left corner (0, 0).

        Returns:    The bounding rectangle
        """
        return Rect((0, 0), self.size)


image_array_cache = {}


def get_image_array(name, shape, **kwds) -> Surface:
    """
    Creates and returns an ImageArray from an image resource with the given name. The ImageArray is cached, and
    subsequent calls with the same name will return the cached object. Additional keyword arguments are
    passed on to ``albow.core.ResourceUtility``.get_image().

    Args:
        name:   The image name

        shape:  The shape

        **kwds:

    Returns:

    """
    result = image_array_cache.get(name)
    if result is None:
        result = ImageArray(ResourceUtility.get_image(name, **kwds), shape)
        image_array_cache[name] = result
    return result
