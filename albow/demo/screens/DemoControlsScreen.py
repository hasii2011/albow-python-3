
from math import pi

from albow.References import AttrRef

from albow.input.FloatField import FloatField

from albow.widgets.ValueDisplay import ValueDisplay

from albow.widgets.Label import Label
from albow.widgets.Button import Button
from albow.widgets.RadioButton import RadioButton
from albow.widgets.ImageButton import ImageButton

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

        contents = DemoControlsScreen.makeContents(self.backButton)

        self.add_centered(contents)

    @classmethod
    def makeContents(cls, backButton: Button = None) -> Column:

        model = DemoControlsModel()

        width_field  = FloatField  (ref=AttrRef(base=model, name='width'))
        height_field = FloatField  (ref=AttrRef(base=model, name='height'))
        area_display = ValueDisplay(ref=AttrRef(base=model, name='area'), format="%.2f")
        shape        = AttrRef(model, 'shape')
        shape_choices = Row([
            RadioButton(setting='rectangle', ref=shape), Label("Rectangle"),
            RadioButton(setting='triangle',  ref=shape), Label("Triangle"),
            RadioButton(setting='ellipse',   ref=shape), Label("Ellipse"),
        ])
        grid = Grid([
            [Label("Width"), width_field],
            [Label("Height"), height_field],
            [Label("Shape"), shape_choices],
            [Label("Value Area"), area_display],
        ])

        imgBtnBall: ImageButton = ImageButton(theImage="ball.gif")
        imgBtnHighlightedBall: ImageButton = ImageButton(theImage="ball.gif", highlightedBgImage="ball_highlighted.png")
        imgBtnDisabledBall: ImageButton = ImageButton(theImage="ball.gif", disabledBgImage="ball_disabled.png", enabled=False)
        imgBtnEnabledBall: ImageButton = ImageButton(theImage="ball.gif", enabledBgImage="ball_enabled.png", enabled=True)

        imgBtnTitle: Label = Label("Image Buttons")
        imgBtnGrid: Grid = Grid([
            [Label("Regular"), imgBtnBall],
            [Label("Highlighted"), imgBtnHighlightedBall],
            [Label("Disabled"), imgBtnDisabledBall],
            [Label("Enabled"), imgBtnEnabledBall]
        ])

        width_field.focus()

        if backButton is None:
            contents = Column([grid, imgBtnTitle, imgBtnGrid])
        else:
            contents = Column([grid, imgBtnTitle, imgBtnGrid, backButton])
        return contents