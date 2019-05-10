
from pygame import Rect

from OpenGL import GLU

from albow.openGL.GLViewport import GLViewport


class GLPerspective(GLViewport):
    """
    `GLPerspective` provides an OpenGL drawing area with a perspective projection.

    Using a GLPerspective widget is the same as using a `GLViewport`, except that you do not need to provide
    a `setup_projection()` method.
    """
    def __init__(self, rect: Rect=None, fovy: int=20, near: float=0.1, far: int=1000, **kwds):
        """
        Creates a GLPerspective instance with the given initial values for its projection parameters.

        The projection parameters, as used by `gluPerspective()`. You can change these to dynamically modify
        the projection. The aspect ratio is calculated automatically from the widget dimensions.

        Args:
            rect:

            fovy:

            near:

            far:

            **kwds:
        """
        #
        # Python 3 update
        #
        # GLViewport.__init__(self, rect, **kwds)
        super().__init__(rect, **kwds)

        self.fovy = fovy
        self.near = near
        self.far = far

    def setup_projection(self):
        aspect = self.width / self.height
        GLU.gluPerspective(self.fovy, aspect, self.near, self.far)
