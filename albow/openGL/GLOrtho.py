
from OpenGL import GL

from albow.openGL.GLViewport import GLViewport


class GLOrtho(GLViewport):

    def __init__(self, rect=None, xmin=-1, xmax=1, ymin=-1, ymax=1, near=-1, far=1, **kwds):

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
