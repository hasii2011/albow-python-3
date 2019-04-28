
import os
import pygame

import logging

from albow.core.Screen import Screen
from albow.core.shell import Shell
from albow.resource import resource_dir

from albow.themes.Theme import Theme
from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.choices.TextMultiChoice import TextMultiChoice
from albow.choices.ImageMultiChoice import ImageMultiChoice

from albow.layout.Column import Column
from albow.layout.Row import Row

IMAGE_RESOURCES_SUBDIR = "images"
DEMO_CHOICE_IMAGE_1    = "EnterpriseD.png"
DEMO_CHOICE_IMAGE_2    = "KlingonD7.png"
DEMO_CHOICE_IMAGE_3    = "medfighter.png"

DEMO_IMAGES = [
    DEMO_CHOICE_IMAGE_1,
    DEMO_CHOICE_IMAGE_2,
    DEMO_CHOICE_IMAGE_3
]
DEMO_IMAGE_VALUES = [
    "Enterprise D",
    "Klingon D7",
    "Med Fighter"
]
class DemoMultiChoiceScreen(Screen):

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)
        screenAttrs = {'bg_color': Theme.WHITE}

        super().__init__(shell=shell, **screenAttrs)

        labelAttrs = {
            'bg_color': Theme.WHITE,
            'fg_color': Theme.BLACK
        }
        textLabel        = Label("Make a choice: ", **labelAttrs)
        textMultiChoice  = self.makeTextMultiChoice()

        imageLabel       = Label("Pick your ship: ", **labelAttrs)
        imageMultiChoice = self.makeImageMultiChoice()

        textRow  = Row([textLabel, textMultiChoice])
        imageRow = Row([imageLabel, imageMultiChoice])

        backButton       = Button("Menu", action=shell.show_menu)

        columnAttrs = {
            "align": "l"
        }
        contents = Column([textRow, imageRow, backButton], **columnAttrs)

        self.add_centered(contents)
        backButton.focus()

    def makeTextMultiChoice(self):

        textValues      = ["Value 1", "Value 2", "Value 3"]
        labelValues     = ["Choice 1", "Choice 2", "Choice 3"]
        textMultiChoice = TextMultiChoice(values=textValues, labels=labelValues)

        return textMultiChoice

    def makeImageMultiChoice(self):

        self.logger.debug("Resource directory: %s", resource_dir)

        pathToImages = resource_dir +"/" + IMAGE_RESOURCES_SUBDIR

        self.logger.debug("Path to images: %s", pathToImages)

        choiceImages = []
        for imageFileName in DEMO_IMAGES:

            imagePath = os.path.join(pathToImages, imageFileName)

            self.logger.debug("Image Path: %s", imagePath)
            choiceImage = pygame.image.load(imagePath)
            choiceImages.append(choiceImage)

        imageMultiChoice = ImageMultiChoice(images=choiceImages, values=DEMO_IMAGE_VALUES)

        return imageMultiChoice