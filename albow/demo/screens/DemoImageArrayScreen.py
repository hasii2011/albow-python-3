
from albow.core.Screen import Screen
from albow.core.shell_tmp import Shell
from albow.resource import get_font

from albow.image_array import get_image_array

from albow.widgets.Label import Label
from albow.widgets.Button import Button
from albow.widgets.Image import Image

from albow.layout.Column import Column

class DemoImageArrayScreen(Screen):
    """
    Image Array
    """

    def __init__(self, shell: Shell):
        Screen.__init__(self, shell)
        self.images = get_image_array("fruit.png", shape=3, border=2)
        self.image = Image(self.images[0])
        self.index = 0
        contents = Column([
            Label("Image Array", font=get_font(18, "VeraBd.ttf")),
            self.image,
            Button("Next Fruit", action=self.next_image),
            Button("Menu", action=shell.show_menu),
        ], spacing=30)
        self.add_centered(contents)

    def next_image(self):
        self.index = (self.index + 1) % 3
        self.image.image = self.images[self.index]

