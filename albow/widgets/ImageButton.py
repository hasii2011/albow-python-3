
from pygame import Surface

from albow.widgets.ButtonBase import ButtonBase
from albow.widgets.Image import Image
from albow.themes.ThemeProperty import ThemeProperty


class ImageButton(ButtonBase, Image):
    """
    TODO:  We need a demo screen for this class

    An ImageButton is a button whose appearance is defined by an image.
    """
    disabled_bg_image    = ThemeProperty('disabled_bg_image')
    """
        This disabled background image
    """
    enabled_bg_image     = ThemeProperty('enabled_bg_image')
    """
    The enabled background image
    """
    highlighted_bg_image = ThemeProperty('highlighted_bg_image')
    """
        The highlighted background image
    """

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
