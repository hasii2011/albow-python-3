
from OpenGL import GLU

from albow.openGL.GLViewport import GLViewport


class GLPerspective(GLViewport):

    def __init__(self, rect=None, fovy=20, near=0.1, far=1000, **kwds):

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
