
from pygame.display import get_surface as get_display

from OpenGL import GL
from OpenGL import GLU

from albow.core.Widget import Widget


class GLViewport(Widget):

    is_gl_container = True

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

    def setup_projection(self):
        pass

    def setup_modelview(self):
        pass

    def gl_draw(self):
        pass

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

