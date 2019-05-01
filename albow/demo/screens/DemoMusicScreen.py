
import logging

from albow.layout.Column import Column

from albow.core.Shell import Shell

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen

class DemoMusicScreen(BaseDemoScreen):

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)

        super().__init__(shell=shell)

        self.logger.info("Use back button: %s", self.backButton)

        columnAttrs = {
            "align": "c",
            'expand': 0
        }
        contents = Column([self.backButton], **columnAttrs)
        self.add_centered(contents)
        self.backButton.focus()

