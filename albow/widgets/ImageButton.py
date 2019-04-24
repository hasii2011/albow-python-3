
from pygame import Surface

from albow.widgets.ButtonBase import ButtonBase
from albow.widgets.Image import Image

from themes.theme_1 import ThemeProperty

class ImageButton(ButtonBase, Image):

    disabled_bg_image    = ThemeProperty('disabled_bg_image')
    enabled_bg_image     = ThemeProperty('enabled_bg_image')
    highlighted_bg_image = ThemeProperty('highlighted_bg_image')

    def draw(self, surface: Surface):

        dbi = self.disabled_bg_image
        ebi = self.enabled_bg_image
        hbi = self.highlighted_bg_image
        # fgi = self.image              Python 3 update, variable unused
        if not self.enabled:
            if dbi:
                self.draw_image(surface, dbi)
        elif self.highlighted:
            if hbi:
                self.draw_image(surface, hbi)
            else:
                surface.fill(self.highlight_color)
        else:
            if ebi:
                self.draw_image(surface, ebi)
        fgi = self.image
        if fgi:
            self.draw_image(surface, fgi)
