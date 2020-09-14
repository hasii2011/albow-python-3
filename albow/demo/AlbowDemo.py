"""
    The Albow Demonstration Program
"""
import json

import pygame
import logging.config

from albow.themes.Theme import Theme
from albow.themes.ThemeLoader import ThemeLoader

JSON_LOGGING_CONFIG_FILENAME = "loggingConfiguration.json"

# SCREEN_SIZE   = (640, 480)
# DISPLAY_FLAGS = pygame.RESIZABLE
DEMO_WINDOW_TITLE       = "Albow Demonstration 2.0"
SCREEN_SIZE             = (960, 480)
DISPLAY_FLAGS           = 0


def main():
    #
    # This has to be done as early as possible to affect the logging
    # statements in the class files
    # Pycharm gives a warning on the order of imports, Oh well
    #

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

    from albow.demo.AlbowDemoShell import AlbowDemoShell

    pygame.init()
    pygame.display.set_caption(f'{DEMO_WINDOW_TITLE}')

    # "file_handler": {
    #   "class": "logging.FileHandler",
    #   "level": "DEBUG",
    #   "formatter": "simple",
    #   "filename": "demo_logging.log",
    #   "encoding": "utf8"
    #   },
    logger  = logging.getLogger(__name__)
    display = pygame.display.set_mode(SCREEN_SIZE, DISPLAY_FLAGS)
    shellArgs = {
        'margin':  5
    }
    shell   = AlbowDemoShell(display, **shellArgs)

    logger.info("Starting %s", __name__)

    shell.run()


if __name__ == '__main__':
    main()
