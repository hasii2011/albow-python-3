
import logging

from albow.core.Shell import Shell

from albow.layout.Column import Column

from albow.widgets.Button import Button

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen

from albow.media.MusicOptionsDialog import MusicOptionsDialog


class DemoMusicScreen(BaseDemoScreen):

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)

        super().__init__(shell=shell)

        self.logger.info("Use back button: %s", self.backButton)

        columnAttrs = {
            "align": "c",
            'expand': 0
        }
        attrs = {
            'font': self.smallButtonFont
        }
        launchMusicDialog: Button = Button(text="Options Dialog", action=self.testOptionsDialog, **attrs)

        contents = Column([launchMusicDialog, self.backButton], **columnAttrs)
        self.add_centered(contents)
        self.backButton.focus()

    def testOptionsDialog(self):

        dialog: MusicOptionsDialog = MusicOptionsDialog()

        dialog.present()