"""
    Albow - Demonstration
"""
import os
import sys

from os.path import dirname as d

import pygame
import logging.config

from albow.demo.DemoShell import DemoShell
# SCREEN_SIZE   = (640, 480)
# DISPLAY_FLAGS = pygame.RESIZABLE
SCREEN_SIZE = (480, 640)
DISPLAY_FLAGS    = 0

sys.path.insert(1, d(d(os.path.abspath(sys.argv[0]))))


def main():

    pygame.init()
    pygame.display.set_caption("Albow Demonstration")

    logging.config.fileConfig('logging.conf')

    logger  = logging.getLogger(__name__)
    display = pygame.display.set_mode(SCREEN_SIZE, DISPLAY_FLAGS)
    shell   = DemoShell(display)

    logger.info("Starting %s", __name__)

    shell.run()


main()
