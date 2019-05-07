
from pygame import Surface

from pygame.event import Event

from albow.core.RootWidget import get_root
from albow.core.RootWidget import get_focus

from albow.dialog.Dialog import Dialog
from albow.themes.ThemeProperty import ThemeProperty


class Menu(Dialog):
    """
    The Menu class provides a drop-down command menu for use with a MenuBar. It can also be used on its
    own as a pop-up menu of selectable items.

    Using Menus
    -----------

    There are two ways that a Menu can be used: as a drop-down menu in a menu bar, or as a stand-alone pop-up menu.

    - To use it as a drop-down menu, simply add it to the menus list of a MenuBar. The menu bar takes care of showing
    and interacting with the menu automatically.

    - To use it as a pop-up menu, you will need to call the present() method, and possibly the find_item_for_key()
    and/or invoke_command() methods yourself

    Menu item specifications
    ------------------------

    When creating the menu, items are specified as a list of tuples:

    ``(text, command_name)``

    where ``text`` is the title to be displayed for the item, optionally followed by a slash and a key
    combination specifier.

    A key combination specifier consists of a single printable ASCII character, optionally preceded by one or more of
    the following modifiers:

        Character   Key
        ^           Shift
        @           Alt or Option

    The command_name is an internal name used to associate the item with handling methods. Two method names are
    derived from the command name: a handler method (suffixed with ``_cmd``) and an enabling method
    (suffixed with ``_enabled``).
    See `albow.menu.MenuBar` for details of how these methods are used.

    An empty tuple may be used to create a separator between groups of menu items.

    Example
    -------
    ```python

    file_menu = Menu('File', [
        ('Open/O', 'open'),
        (),
        ('Save/S', 'save'),
        (Save As/^S', 'save_as')
    ])

    ```

    """
    disabled_color = ThemeProperty('disabled_color')
    """
    The color with which disabled menu items are displayed
    """
    click_outside_response = -1

    def __init__(self, title, items, **kwds):
        """
        Creates a Menu with the specified title and item list. The title is not displayed in the menu itself,
        but is used when the menu is attached to a MenuBar.

        Args:
            title:  The menu title

            items:  The menu items
            **kwds:
        """

        self._hilited    = None
        self._key_margin = None
        self.title       = title
        self.items       = items
        #
        # Python 3 update
        #
        # self._items      = [MenuItem(*item) for item in items]
        self._items = items
        super().__init__(**kwds)

    def show(self, client, pos):
        """

        :param client:
        :param pos:
        :return:
        """

        client = client or get_root()
        #
        # Python 3 update
        #
        aValue = list(client.local_to_global(pos))
        # self.topleft = client.local_to_global(pos)
        self.topleft = aValue
        focus = get_focus()
        font = self.font
        h = font.get_linesize()
        items = self._items
        margin = self.margin
        height = h * len(items) + h
        w1 = w2 = 0
        for item in items:
            item.enabled = self.command_is_enabled(item, focus)
            w1 = max(w1, font.size(item.text)[0])
            w2 = max(w2, font.size(item.keyname)[0])
        width = w1 + 2 * margin
        self._key_margin = width
        if w2 > 0:
            width += w2 + margin
        self.size = (width, height)

        return Dialog.present(self, centered=False)

    def command_is_enabled(self, item, focus):
        cmd = item.command
        if cmd:
            enabler_name = cmd + '_enabled'
            handler = focus
            while handler:
                enabler = getattr(handler, enabler_name, None)
                if enabler:
                    return enabler()
                handler = handler.next_handler()
        return True

    def draw(self, surf: Surface):

        font = self.font
        h = font.get_linesize()
        sep = surf.get_rect()
        sep.height = 1
        colors = [self.disabled_color, self.fg_color]
        bg = self.bg_color
        xt = self.margin
        xk = self._key_margin
        y = h // 2
        hilited = self._hilited
        for item in self._items:
            text = item.text
            if not text:
                sep.top = y + h // 2
                surf.fill(colors[0], sep)
            else:
                if item is hilited:
                    rect = surf.get_rect()
                    rect.top = y
                    rect.height = h
                    surf.fill(colors[1], rect)
                    color = bg
                else:
                    color = colors[item.enabled]
                buf = font.render(item.text, True, color)
                surf.blit(buf, (xt, y))
                keyname = item.keyname
                if keyname:
                    buf = font.render(keyname, True, color)
                    surf.blit(buf, (xk, y))
            y += h

    def mouse_move(self, e):
        self.mouse_drag(e)

    def mouse_drag(self, e):
        item = self.find_enabled_item(e)
        if item is not self._hilited:
            self._hilited = item
            self.invalidate()

    def mouse_up(self, e):
        item = self.find_enabled_item(e)
        if item:
            self.dismiss(self._items.index(item))

    def find_enabled_item(self, e):
        x, y = e.local
        if 0 <= x < self.width:
            h = self.font.get_linesize()
            i = (y - h // 2) // h
            items = self._items
            if 0 <= i < len(items):
                item = items[i]
                if item.enabled:
                    return item

    def find_item_for_key(self, theEvent: Event):
        """
        Given a key event, finds a matching enabled item and returns its index (0-based).

        Args:
            theEvent: The key event to match up against

        Returns:  Returns -1 if no matching item is found or the matching item is not enabled.

        """
        for item in self._items:
            if item.keycode == theEvent.key and item.shift == theEvent.shift and item.alt == theEvent.alt:
                focus = get_focus()
                if self.command_is_enabled(item, focus):
                    return self._items.index(item)
                else:
                    return -1
        return -1

    def get_command(self, i):
        if i >= 0:
            item = self._items[i]
            cmd = item.command
            if cmd:
                return cmd + '_cmd'

    def invoke_item(self, theCommandIndex):
        """
        Locates and calls a command handler for the item with the given index (0-based). Does nothing if
        the index is -1.

        .. Note::
            Does not check whether the item is enabled.

        Args:
            theCommandIndex: The command handler index
        """
        cmd = self.get_command(theCommandIndex)
        if cmd:
            get_focus().handle_command(cmd)
