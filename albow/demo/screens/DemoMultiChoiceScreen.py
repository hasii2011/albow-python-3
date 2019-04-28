
from albow.screen import Screen
from albow.shell import Shell
from albow.themes.Theme import Theme
from albow.widgets.Button import Button

from albow.choices.TextMultiChoice import TextMultiChoice
from albow.layout.Column import Column


class DemoMultiChoiceScreen(Screen):

    def __init__(self, shell: Shell):

        attrs = {'bg_color': Theme.WHITE}

        super().__init__(shell=shell, **attrs)

        textValues      = ["Value 1", "Value 2", "Value 3"]
        labelValues     = ["Choice 1", "Choice 2", "Choice 3"]
        textMultiChoice = TextMultiChoice(values=textValues, labels=labelValues)
        backButton      = Button("Menu", action=shell.show_menu)

        contents = Column([textMultiChoice, backButton])

        self.add_centered(contents)
        backButton.focus()
