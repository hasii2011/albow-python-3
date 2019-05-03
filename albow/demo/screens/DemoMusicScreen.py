
import logging

from albow.core.Shell import Shell

from albow.layout.Column import Column

from albow.widgets.Button import Button

from albow.dialog.DialogUtilities import alert

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen

from albow.media.MusicOptionsDialog import MusicOptionsDialog
from albow.media.PlayList import PlayList

from albow.media.MusicUtilities import MusicUtilities


class DemoMusicScreen(BaseDemoScreen):

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)

        super().__init__(shell=shell)

        columnAttrs = {
            "align": "c",
            'expand': 0
        }
        attrs = {
            'font': self.smallButtonFont
        }
        launchMusicDialogButt: Button = Button(text="Options Dialog", action=DemoMusicScreen.testOptionsDialog, **attrs)
        loadDemoMusicButt:     Button = Button(text="Load Music",     action=DemoMusicScreen.testLoadMusic,     **attrs)
        playMusicButt:         Button = Button(text="Play Music",     action=DemoMusicScreen.playMusic,         **attrs)
        stopMusicButt:         Button = Button(text="Stop Music",     action=DemoMusicScreen.stopMusic,         **attrs)

        contents = Column([launchMusicDialogButt,
                           loadDemoMusicButt,
                           playMusicButt,
                           stopMusicButt,
                           self.backButton], **columnAttrs)
        self.add_centered(contents)
        self.backButton.focus()

    @staticmethod
    def testOptionsDialog():

        dialog: MusicOptionsDialog = MusicOptionsDialog()

        dialog.present()

    @staticmethod
    def testLoadMusic():

        path1 = MusicUtilities.get_music("ElecPiK04 75E-01.mp3")
        path2 = MusicUtilities.get_music("ElecPiK04 75E-02.mp3")
        path3 = MusicUtilities.get_music("ElecPiK04 75E-03.mp3")
        path4 = MusicUtilities.get_music("ElecPiK04 75E-04.mp3")

        MusicUtilities.set_music_enabled(False)
        paths = {path1, path2, path3, path4}
        playList = PlayList(items=paths, random=True, repeat=True)
        MusicUtilities.change_playlist(new_playlist=playList)

        alert("Music Loaded")

    @staticmethod
    def playMusic():

        if MusicUtilities.get_current_playlist() is None:

            alert("Demo music not loaded. Loading my favorite track")

            favPath = MusicUtilities.get_music("Zoe_Poledouris_-_I_Have_Not_Been_To_Paradise_David_Bowie_Cover.mp3")
            paths   = {favPath}
            favPlayList = PlayList(items=paths, random=True, repeat=True)
            favPlayList.repeat = False
            favPlayList.random = False
            MusicUtilities.change_playlist(new_playlist=favPlayList)

        else:
            MusicUtilities.set_music_enabled(True)
            MusicUtilities.start_next_music()

    @staticmethod
    def stopMusic():
        MusicUtilities.music_end()