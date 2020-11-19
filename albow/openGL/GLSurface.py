
from pygame import Rect
from pygame import image

# noinspection PyPackageRequirements
from OpenGL import GL
# noinspection PyPackageRequirements
from OpenGL import GLU


class GLSurface:

    def __init__(self, display, rect):
        self.display = display
        self.rect = rect

    def gl_enter(self):
        r = self.rect
        w = r.width
        h = r.height
        gl = GL
        win_height = self.display.get_height()
        gl.glViewport(r.left, win_height - r.bottom, r.width, r.height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        GLU.gluOrtho2D(0, w, h, 0)
        gl.glMatrixMode(gl.GL_MODELVIEW)
        gl.glLoadIdentity()
        gl.glPushAttrib(gl.GL_COLOR_BUFFER_BIT)
        gl.glDisable(gl.GL_DEPTH_TEST)
        gl.glEnable(gl.GL_BLEND)
        gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

    def gl_exit(self):
        GL.glPopAttrib()

    def gl_clear(self, bg):
        if bg:
            r = bg[0] / 255.0
            g = bg[1] / 255.0
            b = bg[2] / 255.0
            GL.glClearColor(r, g, b, 0.0)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT
                   | GL.GL_ACCUM_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT)

    def gl_flush(self):
        GL.glFlush()

    def get_size(self):
        return self.rect.size

    def get_width(self):
        return self.rect.width

    def get_height(self):
        return self.rect.height

    def get_rect(self):
        return Rect(self.rect)

    def blit(self, src, dst=(0, 0), area=None):

        if isinstance(dst, Rect):
            dst = dst.topleft
        x, y = dst
        if area is not None:
            area = area.clip(src.get_rect())
            src = src.subsurface(area)
            x += area.left
            y += area.top
        w, h = src.get_size()
        data = image.tostring(src, 'RGBA', 1)

        gl = GL
        gl.glRasterPos2i(x, y + h)
        gl.glDrawPixels(w, h, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)

    def fill(self, color, rect=None):

        if rect:
            x, y, w, h = rect
        else:
            x = y = 0
            w, h = self.rect.size
        gl = GL
        gl.glColor4ubv(color)
        gl.glBegin(GL.GL_QUADS)
        v = GL.glVertex2i
        v(x, y)
        v(x+w, y)
        v(x+w, y+h)
        v(x, y+h)
        gl.glEnd()

    def subsurface(self, rect):
        r = self.rect
        subrect = rect.move(r.left, r.top)
        return GLSurface(self.display, r.clip(subrect))
