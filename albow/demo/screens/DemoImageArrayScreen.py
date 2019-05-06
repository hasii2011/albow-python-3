
from albow.core.Shell import Shell

from albow.containers.ImageArray import get_image_array

from albow.widgets.Label import Label
from albow.widgets.Button import Button
from albow.widgets.Image import Image

from albow.layout.Column import Column

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoImageArrayScreen(BaseDemoScreen):
    """
    Image Array
    """

    def __init__(self, shell: Shell):

        super().__init__(shell)
        self.images = get_image_array("fruit.png", shape=3, border=2)
        self.image = Image(self.images[0])
        self.index = 0

        buttAttrs = {
            'font': self.smallButtonFont
        }
        contentAttrs = {
            "align": "c",
            "margin": 10,
            'border_width': 1
        }

        contents = Column([
            Label("Image Array", font=self.labelFont, **self.labelAttrs),
            self.image,
            Button("Next Fruit", action=self.next_image, **buttAttrs),
            self.backButton,
        ], spacing=10, **contentAttrs)

        self.add_centered(contents)

    def next_image(self):
        self.index = (self.index + 1) % 3
        self.image.image = self.images[self.index]

