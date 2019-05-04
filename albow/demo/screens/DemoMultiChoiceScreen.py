
import os
import pygame

import logging

from albow.core.Shell import Shell
from albow.core.ResourceUtility import ResourceUtility

from albow.themes.Theme import Theme
from albow.widgets.Label import Label

from albow.choices.TextMultiChoice import TextMultiChoice
from albow.choices.ImageMultiChoice import ImageMultiChoice

from albow.layout.Column import Column
from albow.layout.Row import Row

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen

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


class DemoMultiChoiceScreen(BaseDemoScreen):

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)

        super().__init__(shell=shell)

        labelAttrs = {
            'bg_color': Theme.WHITE,
            'fg_color': Theme.BLACK
        }
        textLabel        = Label("Make a choice: ", **labelAttrs)
        textMultiChoice  = self.makeTextMultiChoice()

        imageLabel       = Label("Pick your ship: ", **labelAttrs)
        imageMultiChoice = self.makeImageMultiChoice()

        rowAttrs = {
            'spacing': 2
        }
        textRow  = Row([textLabel, textMultiChoice],   **rowAttrs)
        imageRow = Row([imageLabel, imageMultiChoice], **rowAttrs)

        innerColumnAttrs = {
            "align": "l"
        }
        innerColumn: Column = Column([textRow, imageRow], spacing=10, **innerColumnAttrs)

        columnAttrs = {
            "align": "c",
            "margin": 5,
            'border_width': 1
        }
        contents = Column([innerColumn, self.backButton], spacing=10, **columnAttrs)

        self.add_centered(contents)
        self.backButton.focus()

    def makeTextMultiChoice(self):

        textValues      = ["Value 1", "Value 2", "Value 3"]
        labelValues     = ["Choice 1", "Choice 2", "Choice 3"]
        textMultiChoice = TextMultiChoice(values=textValues, labels=labelValues)

        return textMultiChoice

    def makeImageMultiChoice(self):

        self.logger.debug("Resource directory: %s", ResourceUtility.find_resource_dir())

        pathToImages = ResourceUtility.find_resource_dir() + "/" + IMAGE_RESOURCES_SUBDIR

        self.logger.debug("Path to images: %s", pathToImages)

        choiceImages = []
        for imageFileName in DEMO_IMAGES:

            imagePath = os.path.join(pathToImages, imageFileName)

            self.logger.debug("Image Path: %s", imagePath)
            choiceImage = pygame.image.load(imagePath)
            choiceImages.append(choiceImage)

        imageMultiChoice = ImageMultiChoice(images=choiceImages, values=DEMO_IMAGE_VALUES)

        return imageMultiChoice