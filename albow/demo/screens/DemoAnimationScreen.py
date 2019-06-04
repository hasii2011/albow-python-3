
from albow.core.ui.Shell import Shell

from albow.layout.Column import Column

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen
from albow.demo.screens.DemoAnimationWidget import DemoAnimationWidget


class DemoAnimationScreen(BaseDemoScreen):
    """
    Animation
    """

    def __init__(self, shell: Shell):

        super().__init__(shell)

        animationWidget: DemoAnimationWidget = DemoAnimationWidget(shell)

        content: Column = Column([animationWidget, self.backButton])
        self.add(content)
