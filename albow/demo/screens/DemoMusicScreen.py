
import logging

from albow.core.Shell import Shell

from albow.layout.Column import Column

from albow.widgets.Button import Button

from albow.dialog.DialogUtilities import alert

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen

from albow.media.MusicOptionsDialog import MusicOptionsDialog
from albow.media.PlayList import PlayList

from albow.media.EnableMusicControl import change_playlist
from albow.media.EnableMusicControl import get_current_playlist
from albow.media.EnableMusicControl import set_music_enabled
from albow.media.EnableMusicControl import start_next_music

from albow.media.MusicUtilities import get_music

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
        launchMusicDialogButt: Button = Button(text="Options Dialog", action=self.testOptionsDialog, **attrs)
        loadDemoMusicButt:     Button = Button(text="Load Music",     action=self.testLoadMusic,     **attrs)
        playMusicButt:         Button = Button(text="Play Music",     action=self.playMusic,         **attrs)

        contents = Column([launchMusicDialogButt,
                           loadDemoMusicButt,
                           playMusicButt,
                           self.backButton], **columnAttrs)
        self.add_centered(contents)
        self.backButton.focus()

    def testOptionsDialog(self):

        dialog: MusicOptionsDialog = MusicOptionsDialog()

        dialog.present()

    def testLoadMusic(self):

        path1 = get_music("ElecPiK04 75E-01.mp3")
        path2 = get_music("ElecPiK04 75E-02.mp3")
        path3 = get_music("ElecPiK04 75E-03.mp3")
        path4 = get_music("ElecPiK04 75E-04.mp3")

        set_music_enabled(False)
        paths = {path1, path2, path3, path4}
        playList = PlayList(items=paths, random=True, repeat=True)
        change_playlist(new_playlist=playList)

        alert("Music Loaded")

    def playMusic(self):

        if get_current_playlist() == None:
            alert("Please load music")
        else:
            set_music_enabled(True)
            start_next_music()
