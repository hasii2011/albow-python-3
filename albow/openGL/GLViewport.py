
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

    # Looks obsolete -- hasii
    # def gl_draw_self(self, root, offset):
    #     rect = self.rect.move(offset)

    def gl_draw_self(self, gl_surface):
        """

        Args:
            gl_surface:

        Returns:

        """
        #
        # GL_CLIENT_ALL_ATTRIB_BITS is borked: defined as -1 but
        # glPushClientAttrib insists on an unsigned long.
        #
        GL.glPushClientAttrib(0xffffffff)
        GL.glPushAttrib(GL.GL_ALL_ATTRIB_BITS)
        # GL.glViewport(rect.left, root.height - rect.bottom, rect.width, rect.height)
        self.gl_draw_viewport()
        GL.glPopAttrib()
        GL.glPopClientAttrib()

    def gl_draw_viewport(self):
        """
        This method is called after the viewport has been set up. It is responsible for establishing the
        projection and modelview matrices and performing the drawing. All OpenGL attributes are saved
        and restored around calls to this method. The default implementation calls `setup_matrices()` and `gl_draw()`.

        """
        self.setup_matrices()
        self.gl_draw()

    def setup_matrices(self):
        """
        This method is called from the default implementation of `gl_draw_viewport()`. It is responsible for setting
        up the projection and modelview matrices. The default implementation calls `setup_projection()` and
        `setup_modelview()`.

        """
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
        """
        This method is used to add the ray attribute to a mouse event before calling the corresponding handler.
        Usually it is called automatically, but you may want to call it yourself if you receive a mouse event by
        some means other than the usual channels. Note: This method calls the matrix setup methods, and changes
        the projection and modelview matrices as a side effect.

        Args:
            event:  The event to augment

        Returns:  a modified event

        """
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
