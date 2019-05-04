
from pygame import Rect

from albow.openGL.GLOrtho import GLOrtho

from OpenGL.GL import glBegin
from OpenGL.GL import glColor3f
from OpenGL.GL import glVertex2f
from OpenGL.GL import glEnd
from OpenGL.GL import GL_TRIANGLES


class OrthoDemo(GLOrtho):

    sat = 1.0

    def __init__(self):
        GLOrtho.__init__(self, Rect(0, 0, 200, 200), 0, 10, 0, 10)

    def gl_draw(self):
        s = 1.0 - self.sat
        glBegin(GL_TRIANGLES)
        glColor3f(1, s, s)
        glVertex2f(5, 10)
        glColor3f(s, 1, s)
        glVertex2f(0, 0)
        glColor3f(s, s, 1)
        glVertex2f(10, 0)
        glEnd()

    def lighter(self):
        self.sat = max(0.0, self.sat - 0.1)

    def darker(self):
        self.sat = min(1.0, self.sat + 0.1)
