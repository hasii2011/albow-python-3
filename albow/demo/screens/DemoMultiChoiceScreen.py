
import os
import pygame

import logging
from logging import Logger

from albow.core.ui.Shell import Shell
from albow.core.ResourceUtility import ResourceUtility

from albow.widgets.Label import Label
from albow.widgets.Button import Button

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

    classLogger: Logger = logging.getLogger(__name__)

    def __init__(self, shell: Shell):

        super().__init__(shell=shell)

        contents = DemoMultiChoiceScreen.makeContents(backButton=self.backButton)
        self.add_centered(contents)
        self.backButton.focus()

    @classmethod
    def makeContents(cls, backButton: Button = None) -> Column:

        textLabel       = Label("Make a choice: ")
        textMultiChoice = cls.makeTextMultiChoice()

        imageLabel       = Label("Pick your ship: ")
        imageMultiChoice = cls.makeImageMultiChoice()

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
        if backButton is None:
            # contents = Column([innerColumn, self.backButton], spacing=10, **columnAttrs)
            contents = innerColumn
        else:
            contents = Column([innerColumn, backButton], spacing=10, **columnAttrs)

        return contents

    @classmethod
    def makeTextMultiChoice(cls):

        textValues      = ["Value 1", "Value 2", "Value 3"]
        labelValues     = ["Choice 1", "Choice 2", "Choice 3"]
        textMultiChoice = TextMultiChoice(values=textValues, labels=labelValues)

        return textMultiChoice

    @classmethod
    def makeImageMultiChoice(cls):

        cls.classLogger.debug(f"Resource directory: {ResourceUtility.find_resource_dir()}")

        pathToImages = ResourceUtility.find_resource_dir() + "/" + IMAGE_RESOURCES_SUBDIR

        cls.classLogger.debug(f"Path to images: {pathToImages}")

        choiceImages = []
        for imageFileName in DEMO_IMAGES:

            imagePath = os.path.join(pathToImages, imageFileName)

            cls.classLogger.debug(f"Image Path: {imagePath}")
            choiceImage = pygame.image.load(imagePath)
            choiceImages.append(choiceImage)

        imageMultiChoice = ImageMultiChoice(images=choiceImages, values=DEMO_IMAGE_VALUES)

        return imageMultiChoice
