
screen_size = (640, 480)
flags = 0

import os
import sys

from os.path import dirname as d
sys.path.insert(1, d(d(os.path.abspath(sys.argv[0]))))

from OpenGL.GL import *

import pygame

pygame.init()

from pygame.color import Color
from pygame.locals import *

from albow.core.RootWidget import RootWidget

from albow.widgets.Button import Button
from albow.layout.Row import Row

from albow.openGL.GLOrtho import GLOrtho
from albow.openGL.GLPerspective import GLPerspective


class DemoButton(Button):
    bg_color = Color("brown")
    border_width = 2
    margin = 4


class OrthoDemo(GLOrtho):

    sat = 1.0

    def __init__(self):
        GLOrtho.__init__(self,
                         Rect(0, 0, 200, 200),
                         0, 10, 0, 10)

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


def ortho_controls(ortho):
    bl = DemoButton("Lighter", ortho.lighter)
    bd = DemoButton("Darker", ortho.darker)
    row = Row([bl, bd])
    return row


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
        GLPerspective.__init__(self, Rect(0, 0, 200, 200))

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

    def mouse_down(self, e):
        print("Perspective: mouse_down: ray =", e.ray)

    def rot(self, i):
        self.arot[i] = (self.arot[i] + 10) % 360


def persp_controls(persp):
    bx = DemoButton("RotX", lambda: persp.rot(0))
    by = DemoButton("RotY", lambda: persp.rot(1))
    bz = DemoButton("RotZ", lambda: persp.rot(2))
    row = Row([bx, by, bz])
    return row


def add_demo_widgets(root):
    ortho = OrthoDemo()
    ortho.topleft = (20, 20)
    root.add(ortho)
    ocon = ortho_controls(ortho)
    ocon.midtop = (ortho.centerx, ortho.bottom + 20)
    root.add(ocon)
    persp = PerspectiveDemo()
    persp.topleft = (ortho.right + 20, ortho.top)
    root.add(persp)
    pcon = persp_controls(persp)
    pcon.midtop = (persp.centerx, persp.bottom + 20)
    root.add(pcon)


def main():
    gl_flags = flags | OPENGL
    if "-s" in sys.argv:
        print("Using single buffering")
    else:
        print("Using double buffering")
        gl_flags |= DOUBLEBUF
    display = pygame.display.set_mode(screen_size, gl_flags)
    root = RootWidget(display)
    root.bg_color = Color("blue")
    add_demo_widgets(root)
    root.run()

if __name__ == '__main__':
    main()
