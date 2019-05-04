
from pygame import Rect

from OpenGL.GL import glBegin
from OpenGL.GL import glEnable
from OpenGL.GL import glTranslatef
from OpenGL.GL import glRotatef
from OpenGL.GL import glColor3fv
from OpenGL.GL import glVertex3fv

from OpenGL.GL import glEnd
from OpenGL.GL import GL_DEPTH_TEST
from OpenGL.GL import GL_QUADS

from albow.openGL.GLPerspective import GLPerspective

cube_pts = [
    (-1, -1, -1), (1, -1, -1), (1, 1, -1), (-1, 1, -1),
    (-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
]

cube_faces = [
    (0, 3, 2, 1), (4, 5, 6, 7),
    (0, 1, 5, 4), (2, 3, 7, 6),
    (1, 2, 6, 5), (0, 4, 7, 3),
]

cube_colors = [
    (1, 0, 0), (0, 1, 0), (0.5, 0.75, 1),
    (1, 1, 0), (1, 0, 1), (0, 1, 1),
]


class PerspectiveDemo(GLPerspective):

    arot = [30, 30, 0]

    def __init__(self):
        #
        # Python 3 update
        #
        super().__init__(Rect(0, 0, 200, 200))

    def gl_draw(self):
        glEnable(GL_DEPTH_TEST)
        glTranslatef(0, 0, -10)
        glRotatef(self.arot[0], 1, 0, 0)
        glRotatef(self.arot[1], 0, 1, 0)
        glRotatef(self.arot[2], 0, 0, 1)
        glBegin(GL_QUADS)

        for aColor, face in zip(cube_colors, cube_faces):
            glColor3fv(aColor)
            for i in face:
                glVertex3fv(cube_pts[i])
        glEnd()

    @staticmethod
    def mouse_down(e):
        print("Perspective: mouse_down: ray =", e.ray)

    def rotate(self, i):
        self.arot[i] = (self.arot[i] + 10) % 360
