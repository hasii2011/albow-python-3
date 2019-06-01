"""
    The Albow OpenGL Demonstration program
"""
import sys

import json

import logging.config

import pygame

from pygame import Surface

from pygame.color import Color
from pygame.locals import OPENGL
from pygame.locals import DOUBLEBUF

from albow.themes.Theme import Theme
from albow.themes.ThemeLoader import ThemeLoader

from albow.core.ui.RootWidget import RootWidget

from albow.layout.Row import Row

from albow.demo.openGL.OrthoDemo import OrthoDemo
from albow.demo.openGL.PerspectiveDemo import PerspectiveDemo
from albow.demo.openGL.DemoButton import DemoButton

JSON_LOGGING_CONFIG_FILENAME = "../loggingConfiguration.json"

def ortho_controls(ortho: OrthoDemo) -> Row:

    bl = DemoButton("Lighter", ortho.lighter)
    bd = DemoButton("Darker", ortho.darker)
    row = Row([bl, bd])

    return row


def perspective_controls(perspectiveDemo: PerspectiveDemo) -> Row:

    bx = DemoButton("RotX", lambda: perspectiveDemo.rotate(0))
    by = DemoButton("RotY", lambda: perspectiveDemo.rotate(1))
    bz = DemoButton("RotZ", lambda: perspectiveDemo.rotate(2))
    row = Row([bx, by, bz])

    return row


def add_demo_widgets(root: RootWidget):

    orthoDemo: OrthoDemo = OrthoDemo()
    orthoDemo.topleft = (20, 20)
    root.add(orthoDemo)

    orthoControls = ortho_controls(orthoDemo)
    orthoControls.midtop = (orthoDemo.centerx, orthoDemo.bottom + 20)
    root.add(orthoControls)

    perspectiveDemo = PerspectiveDemo()
    perspectiveDemo.topleft = (orthoDemo.right + 20, orthoDemo.top)
    root.add(perspectiveDemo)

    perspectiveControls = perspective_controls(perspectiveDemo)
    perspectiveControls.midtop = (perspectiveDemo.centerx, perspectiveDemo.bottom + 20)
    root.add(perspectiveControls)


screen_size = (640, 480)
flags = 0


def main():

    with open(JSON_LOGGING_CONFIG_FILENAME, 'r') as loggingConfigurationFile:
        configurationDictionary = json.load(loggingConfigurationFile)

    logging.config.dictConfig(configurationDictionary)
    logging.logProcesses = False
    logging.logThreads = False

    #
    # Have to get all the theme attributes defined first before
    # anything is imported with ThemeProperty attributes
    #
    themeLoader: ThemeLoader = ThemeLoader()
    themeLoader.load()
    themeRoot: Theme = themeLoader.themeRoot
    Theme.setThemeRoot(themeRoot)

    pygame.init()

    gl_flags = flags | OPENGL

    if "-s" in sys.argv:
        print("Using single buffering")
    else:
        print("Using double buffering")
        gl_flags |= DOUBLEBUF

    display:       Surface    = pygame.display.set_mode(screen_size, gl_flags)
    root:          RootWidget = RootWidget(display)
    root.bg_color: Color = Color("blue")

    add_demo_widgets(root)

    root.run()


if __name__ == '__main__':
    main()
