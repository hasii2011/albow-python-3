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
LOGGING_CONFIG_FILENAME = "logging.conf"
DEMO_WINDOW_TITLE       = "Albow Demonstration"
SCREEN_SIZE             = (480, 640)
DISPLAY_FLAGS           = 0

sys.path.insert(1, d(d(os.path.abspath(sys.argv[0]))))


def main():

    pygame.init()
    pygame.display.set_caption("%s" % DEMO_WINDOW_TITLE)

    logging.config.fileConfig("%s" % LOGGING_CONFIG_FILENAME)

    logger  = logging.getLogger(__name__)
    display = pygame.display.set_mode(SCREEN_SIZE, DISPLAY_FLAGS)
    shell   = DemoShell(display)

    logger.info("Starting %s", __name__)

    shell.run()


main()
