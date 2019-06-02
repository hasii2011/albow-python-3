
from albow.core.ui.Shell import Shell

from albow.containers.ImageArray import ImageArray

from albow.widgets.Label import Label
from albow.widgets.Button import Button
from albow.widgets.Image import Image

from albow.layout.Column import Column

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoImageArrayScreen(BaseDemoScreen):
    """
    Image Array
    """

    images: ImageArray = None
    image = None
    index: int = 0

    def __init__(self, shell: Shell):

        super().__init__(shell)

        contents: Column = DemoImageArrayScreen.makeContents(self.backButton)
        self.add_centered(contents)

    @classmethod
    def makeContents(cls, backButton: Button=None) -> Column:

        cls.images = ImageArray.get_image_array("fruit.png", shape=3, border=2)
        cls.image = Image(cls.images[0])
        cls.index = 0


        if backButton is None:
            contents: Column = Column([cls.image, Button("Next Fruit", action=cls.next_image),], spacing=10)
        else:
            contentAttrs = {
                "align"       : "c",
                "margin"      : 10,
                'border_width': 1
            }

            contents: Column = Column([
                Label("Image Array"),
                cls.image,
                Button("Next Fruit", action=cls.next_image),
                backButton,
            ], spacing=10, **contentAttrs)

        return contents

    @classmethod
    def next_image(cls):

        cls.index = (cls.index + 1) % 3
        cls.image.image = cls.images[cls.index]
