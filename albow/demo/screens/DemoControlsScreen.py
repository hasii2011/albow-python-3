
from math import pi

from albow.core.Screen import Screen
from albow.legacyReferences import AttrRef

from albow.themes.Theme import Theme

from albow.input.FloatField import FloatField

from albow.widgets.ValueDisplay import ValueDisplay
from albow.widgets.Button import Button
from albow.widgets.Label import Label
from albow.widgets.RadioButton import RadioButton

from albow.layout.Column import Column
from albow.layout.Grid import Grid
from albow.layout.Row import Row

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen

class DemoControlsModel:

    width = 0.0
    height = 0.0
    shape = 'rectangle'

    def get_area(self):
        a = self.width * self.height
        shape = self.shape
        if shape == 'rectangle':
            return a
        elif shape == 'triangle':
            return 0.5 * a
        elif shape == 'ellipse':
            return 0.25 * pi * a

    area = property(get_area)


class DemoControlsScreen(BaseDemoScreen):
    """
    Controls
    """

    def __init__(self, shell):

        """

        :param shell:
        """
        super().__init__(shell)

        model= DemoControlsModel()

        colors = {'border_color': Theme.WHITE,
                  'fg_color':     Theme.BLACK,
                  'bg_color':     Theme.WHITE
                  }
        width_field  = FloatField  (ref=AttrRef(model, 'width'),  **colors)
        height_field = FloatField  (ref=AttrRef(model, 'height'), **colors)
        area_display = ValueDisplay(ref=AttrRef(model, 'area'), format="%.2f", **colors)
        shape        = AttrRef(model, 'shape')
        shape_choices = Row([
            RadioButton(setting='rectangle', ref=shape), Label("Rectangle", **colors),
            RadioButton(setting='triangle',  ref=shape), Label("Triangle",  **colors),
            RadioButton(setting='ellipse',   ref=shape), Label("Ellipse",   **colors),
        ])
        grid = Grid([
            [Label("Width",      **colors), width_field],
            [Label("Height",     **colors), height_field],
            [Label("Shape",      **colors), shape_choices],
            [Label("Value Area", **colors), area_display],
        ])

        contents = Column([grid, self.backButton])
        self.add_centered(contents)
        width_field.focus()
