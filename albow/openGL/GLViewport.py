
from pygame import Rect

from pygame.display import get_surface as get_display

from OpenGL import GL
from OpenGL import GLU

from albow.core.Widget import Widget


class GLViewport(Widget):
    """
    A `GLViewport` provides basic OpenGL drawing and input handling facilities.

    When using 'GLViewport' you are responsible for setting up the projection matrix. For most applications
    you will probably find it more convenient to use `albow.openGL.GLOrtho` or `albow.openGL.GLPerspective`.

    **Mouse Event Handling**

    Mouse events passed to the mouse handling methods of a GLViewport have an additional attribute called
    ray. This is a pair of points __((x1, y1, z1), (x2, y2, z2))__ obtained by projecting the mouse coordinates
    onto the near and far planes respectively.

    The following methods implement the default drawing mechanism.

    - `gl_draw_viewport`
    - `setup_matrices`

    You can optionally override them to gain more control over the process.

    """
    is_gl_container = True

    def __init__(self, rect: Rect = None, **kwds):
        """


        """
        super().__init__(rect, **kwds)

    def gl_draw_self(self, root, offset):
        rect = self.rect.move(offset)

    def gl_draw_self(self, gl_surface):
        # GL_CLIENT_ALL_ATTRIB_BITS is borked: defined as -1 but
        # glPushClientAttrib insists on an unsigned long.
        GL.glPushClientAttrib(0xffffffff)
        GL.glPushAttrib(GL.GL_ALL_ATTRIB_BITS)
        # GL.glViewport(rect.left, root.height - rect.bottom, rect.width, rect.height)
        self.gl_draw_viewport()
        GL.glPopAttrib()
        GL.glPopClientAttrib()

    def gl_draw_viewport(self):
        self.setup_matrices()
        self.gl_draw()

    def setup_matrices(self):
        rect = self.get_global_rect()
        win_height = get_display().get_height()
        GL.glViewport(rect.left, win_height - rect.bottom, rect.width, rect.height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        self.setup_projection()
        GL.glMatrixMode(GL.GL_MODELVIEW)
        GL.glLoadIdentity()
        self.setup_modelview()

    def augment_mouse_event(self, event):
        Widget.augment_mouse_event(self, event)
        w, h = self.size
        viewport = (0, 0, w, h)
        self.setup_matrices()
        # gf = GL.glGetFloatv
        gf = GL.glGetDoublev
        pr_mat = gf(GL.GL_PROJECTION_MATRIX)
        mv_mat = gf(GL.GL_MODELVIEW_MATRIX)
        x, y = event.local
        y = h - y
        up = GLU.gluUnProject
        p0 = up(x, y, 0.0, mv_mat, pr_mat, viewport)
        p1 = up(x, y, 1.0, mv_mat, pr_mat, viewport)
        event.dict['ray'] = (p0, p1)

    #
    # Abstract methods follow
    #
    def setup_projection(self):
        """
        This method is called during drawing and mouse event handling to establish the projection matrix. When
        called, the projection matrix is selected and has been initialized to an identity matrix.
        """
        pass

    def setup_modelview(self):
        """
        This method is called during drawing and mouse event handling to establish the _modelview_ matrix. When
        called, the _modelview_ matrix is selected and has been initialized to an identity matrix.
        """
        pass

    def gl_draw(self):
        """
        This method is called after the projection and model-view matrices have been set up. All OpenGL attributes
        are saved before calling this method and restored afterwards, so you can freely change OpenGL state here
        without affecting any other `GLViewport`s.
        """
        pass

