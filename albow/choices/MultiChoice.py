
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT

from albow.widgets.Control import Control
from albow.containers.PaletteView import PaletteView
from albow.themes.ThemeProperty import ThemeProperty


class MultiChoice(PaletteView, Control):

    highlight_color = ThemeProperty('highlight_color')
    cell_margin = ThemeProperty('cell_margin')

    align = 'c'
    tab_stop = True

    def __init__(self, cell_size, values, **kwds):
        PaletteView.__init__(self, cell_size, 1, len(values), **kwds)
        self.values = values

    def num_items(self):
        return len(self.values)

    def item_is_selected(self, n):
        return self.get_value() == self.values[n]

    def click_item(self, n, e):
        if self.tab_stop:
            self.focus()
        self.set_value(self.values[n])

    def draw(self, surf):
        if self.has_focus():
            surf.fill(self.highlight_color)
        PaletteView.draw(self, surf)

    def key_down(self, e):
        k = e.key
        if k == K_LEFT:
            self.change_value(-1)
        elif k == K_RIGHT:
            self.change_value(1)
        else:
            PaletteView.key_down(self, e)

    def change_value(self, d):
        values = self.values
        if values:
            n = len(values)
            value = self.get_value()
            try:
                i = values.index(value)
            except ValueError:
                if d < 0:
                    i = 0
                else:
                    i = n - 1
            else:
                i = max(0, min(n - 1, i + d))
            self.set_value(values[i])
