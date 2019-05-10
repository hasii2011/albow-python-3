
from pygame import Rect

from OpenGL import GL

from albow.openGL.GLViewport import GLViewport


class GLOrtho(GLViewport):
    """
    GLOrtho provides an OpenGL drawing area with an orthographic projection.

    Using a GLOrtho widget is the same as using a GLViewport, except that you do not need to
    provide a `setup_projection()` method.

    ------

    ------

    """
    def __init__(self, rect: Rect=None, xmin=-1, xmax=1, ymin=-1, ymax=1, near=-1, far=1, **kwds):
        """
        Creates a GLOrtho instance with the given initial values for its projection parameters.

        Args:
            rect:   A pygame Rect

            xmin:   Specify the coordinates for the left vertical clipping planes.

            xmax:   Specify the coordinates for the right vertical clipping planes.

            ymin:   Specify the coordinates for the bottom horizontal clipping planes.

            ymax:   Specify the coordinates for the top horizontal clipping planes.

            near:   Specify the distances to the nearer clipping planes.
                These distances are negative if the plane is to be behind the viewer.

            far:    Specify the distances to the depth clipping planes.
                These distances are negative if the plane is to be behind the viewer.

            **kwds:
        """
        #
        # Python 3 update
        #
        # GLViewport.__init__(self, rect, **kwds)
        super().__init__(rect, **kwds)

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.near = near
        self.far = far

    def setup_projection(self):
        GL.glOrtho(self.xmin, self.xmax, self.ymin, self.ymax, self.near, self.far)
