
from albow.core.RootWidget import get_root
from albow.core.RootWidget import get_focus

from albow.dialog.Dialog import Dialog
from albow.themes.ThemeProperty import ThemeProperty
from albow.menu.MenuItem import MenuItem


class Menu(Dialog):

    disabled_color = ThemeProperty('disabled_color')
    click_outside_response = -1

    def __init__(self, title, items, **kwds):

        self._hilited    = None
        self._key_margin = None
        self.title       = title
        self.items       = items
        #
        # Python 3 update
        #
        # self._items      = [MenuItem(*item) for item in items]
        self._items      = items
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

    def draw(self, surf):
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

    def find_item_for_key(self, e):
        for item in self._items:
            if item.keycode == e.key \
                    and item.shift == e.shift and item.alt == e.alt:
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

    def invoke_item(self, i):
        cmd = self.get_command(i)
        if cmd:
            get_focus().handle_command(cmd)
