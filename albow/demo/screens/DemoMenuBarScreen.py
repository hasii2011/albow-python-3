
import logging

from albow.themes.Theme import Theme

from albow.core.Shell import Shell

from albow.widgets.Button import Button

from albow.layout.Column import Column
from albow.layout.Frame import Frame

from albow.menu.MenuBar import MenuBar
from albow.menu.Menu import Menu
from albow.menu.MenuItem import MenuItem

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoMenuBarScreen(BaseDemoScreen):

    def __init__(self, shell: Shell):

        self.logger = logging.getLogger(__name__)

        super().__init__(shell=shell)

        items = [
            MenuItem(text="Item 1", command="menuItem1"),
            MenuItem(text="Item 2", command="menuItem2"),
            MenuItem(text="Item 3", command="menuItem3"),
            MenuItem(text="Item 4", command="menuItem4")
        ]
        fileMenu = Menu(title="File", items=items)
        editMenu = Menu(title="Edit", items=items)
        viewMenu = Menu(title="View", items=items)
        helpMenu = Menu(title="Help", items=items)
        menus = [
            fileMenu, editMenu, viewMenu, helpMenu
        ]

        menuBar = MenuBar(menus=menus, width=self.width/2)

        framedMenuBar = Frame(client=menuBar)
        columnAttrs = {
            "align": "l",
            'expand': 0
        }
        contents = Column([framedMenuBar, self.backButton], **columnAttrs)

        self.add_centered(contents)
        self.backButton.focus()

    def menuItem1_cmd(self):
        self.logger.info("Executed menu item 1 command")

    def menuItem2_cmd(self):
        self.logger.info("Executed menu item 2 command")

    def menuItem3_cmd(self):
        self.logger.info("Executed menu item 3 command")

    def menuItem4_cmd(self):
        self.logger.info("Executed menu item 4 command")
