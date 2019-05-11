
from typing import List

from pygame import Rect

from albow.utils import overridable_property

from albow.core.Widget import Widget

from albow.menu.Menu import Menu


class MenuBar(Widget):
    """
    The MenuBar class works in conjunction with the Menu class to provide a set of drop-down menus.

    A menu bar displays the titles of its attached menus in a horizontal row. Clicking on a menu title causes
    the associated menu to be displayed, allowing an item to be selected from it.

    Menu items are linked to handler methods via command names. When a menu item is invoked, a search is made
    for a method whose name is the item's command name with ``_cmd`` appended. The search starts at the widget
    having the keyboard focus and proceeds up towards to the root widget.

    Menu items can be enabled or disabled. Whether an item is enabled is determined by searching for an enabling
    method whose name is the command name with ``_enabled`` appended. The search is made along the same path as
    the search for a handler method. If an enabling method is found, it is called and its boolean result
    determines whether the item is enabled. If no enabling method is found, the item defaults to being enabled.

    A menu item can also be associated with a key combination that includes the platform's standard menu
    command modifier key (Command on Mac, Control on other platforms). For this to work, the MenuBar must be
    attached to the menu_bar property of another widget and that widget must be somewhere on the path from
    the root widget to the widget having the keyboard focus.

    .. Note::
        Menu command key events are intercepted while being dispatched from the root down to the
        focus widget.  Thus, menu commands will take precedence over any handling of the same events in key_down
        methods.


    .. Tip:: See Also
        - Menu for details of creating menu items and associating them with command names and key combinations.
        - `albow.core.Widget.menu_bar` for attaching the menu bar to a widget.

    """
    menus: List[Menu] = overridable_property('menus', "List of Menu instances")
    """
    A list of `albow.menu.Menu` instances
    """

    def __init__(self, menus: List[Menu]=None, width=0, **kwds):
        """
        Creates a menu bar. The height defaults to the font height.

        Args:
            menus:  The list of menus to include in the menubar

            width:  If you don't specify a width, it will be set automatically when the menu bar is assigned to
            the menu_bar property of a widget.

            **kwds:
        """
        font = self.predict_font(kwds)
        height = font.get_linesize()

        super().__init__(Rect(0, 0, width, height), **kwds)

        self._menus = menus or []
        self._hilited_menu = None

    def get_menus(self):
        return self._menus

    def set_menus(self, x):
        self._menus = x

    def draw(self, surf):
        fg = self.fg_color
        bg = self.bg_color
        font = self.font
        hilited = self._hilited_menu
        x = 0
        for menu in self._menus:
            text = " %s " % menu.title
            if menu is hilited:
                buf = font.render(text, True, bg, fg)
            else:
                buf = font.render(text, True, fg, bg)
            surf.blit(buf, (x, 0))
            x += buf.get_width()

    def mouse_down(self, e):
        mx = e.local[0]
        font = self.font
        x = 0
        for menu in self._menus:
            text = " %s " % menu.title
            w = font.size(text)[0]
            if x <= mx < x + w:
                self.show_menu(menu, x)
                return
            x += w

    def show_menu(self, menu, x):
        self._hilited_menu = menu
        try:
            i = menu.show(self, (x, self.height))
        finally:
            self._hilited_menu = None
        menu.invoke_item(i)

    def handle_command_key(self, e):

        menus = self.menus
        #
        # Python 3 update -- hasii
        #
        # for m in xrange(len(menus)-1, -1, -1):
        for m in range(len(menus) - 1, -1, -1):
            menu = menus[m]
            i = menu.find_item_for_key(e)
            if i >= 0:
                menu.invoke_item(i)
                return True
        return False
