
import logging

from albow.themes.Theme import Theme

from albow.core.Screen import Screen
from albow.core.Shell import Shell

from albow.widgets.Button import Button

from albow.layout.Column import Column
from albow.layout.Frame import Frame

from albow.menu.MenuBar import MenuBar
from albow.menu.Menu import Menu
from albow.menu.MenuItem import MenuItem


class DemoMenuBarScreen(Screen):

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)
        screenAttrs = {'bg_color': Theme.WHITE}

        super().__init__(shell=shell, **screenAttrs)

        items = [
            MenuItem(text="Item 1"),
            MenuItem(text="Item 2"),
            MenuItem(text="Item 3"),
            MenuItem(text="Item 4")
        ]
        fileMenu = Menu(title="File", items=items)
        editMenu = Menu(title="Edit", items=items)
        viewMenu = Menu(title="View", items=items)
        helpMenu = Menu(title="Help", items=items)
        menus = [
            fileMenu, editMenu, viewMenu, helpMenu
        ]

        menuBar = MenuBar(menus=menus, width=self.width/2)
        backButton = Button("Menu", action=shell.show_menu)

        framedMenuBar = Frame(client=menuBar)
        columnAttrs = {
            "align": "l",
            'expand': 0
        }
        contents = Column([framedMenuBar, backButton], **columnAttrs)

        self.add_centered(contents)
        backButton.focus()
