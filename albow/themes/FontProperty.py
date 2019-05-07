
from albow.themes.Theme import themeRoot

from albow.themes.ThemeProperty import ThemeProperty



class FontProperty(ThemeProperty):
    """
    The FontProperty class is a property descriptor used for defining theme properties whose values are font objects.

    Rather than an actual font object, the corresponding attribute of a Theme object should contain a
    tuple (size, filename) specifying the font. The first time the font property is accessed for a
    given instance, the FontProperty descriptor loads the font using get_font and caches the resulting font object.

    Example
    --------
    ```python
        class DramaticScene(Widget):

        villain_gloat_font = FontProperty('villain_gloat_font')

        from albow.themes.Theme import themeRoot

        themeRoot.DramaticScene = theme.Theme('DramaticScene')
        themeRoot.DramaticScene.villain_gloat_font = (27, "EvilLaughter.ttf")
    ```

    """
    def __init__(self, name):
        """
        Constructs a font property descriptor.
        Args:
            name: Normally name should be the same as the name being used for the property.
        """
        super().__init__(name)

    def get_from_theme(self, cls, name):
        return themeRoot.get_font(cls, name)
