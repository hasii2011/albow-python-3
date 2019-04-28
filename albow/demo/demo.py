"""
    Albow - Demonstration
"""
import os
import sys

from os.path import dirname

import pygame
import logging.config

LOGGING_CONFIG_FILENAME = "logging.conf"
#
# This has to be done as early as possible to affect the logging
# statements in the class files
# Pycharm gives a warning on the order of imports, Oh well
#
logging.config.fileConfig("%s" % LOGGING_CONFIG_FILENAME)
logging.logProcesses = False
logging.logThreads   = False


from albow.demo.DemoShell import DemoShell
# SCREEN_SIZE   = (640, 480)
# DISPLAY_FLAGS = pygame.RESIZABLE
DEMO_WINDOW_TITLE       = "Albow Demonstration"
SCREEN_SIZE             = (480, 640)
DISPLAY_FLAGS           = 0

WTH = dirname(dirname(os.path.abspath(sys.argv[0])))
sys.path.insert(1, WTH)

def main():

    pygame.init()
    pygame.display.set_caption("%s" % DEMO_WINDOW_TITLE)

    logger  = logging.getLogger(__name__)
    display = pygame.display.set_mode(SCREEN_SIZE, DISPLAY_FLAGS)
    shell   = DemoShell(display)

    logger.info("Starting %s", __name__)

    shell.run()

main()