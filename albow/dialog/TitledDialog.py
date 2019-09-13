
from typing import cast

from logging import Logger
from logging import getLogger

from albow.themes.Theme import Theme
from albow.themes.ThemeProperty import ThemeProperty

from albow.widgets.WidgetUtilities import wrapped_label
from albow.dialog.Dialog import Dialog
from albow.dialog.DialogTitleBar import DialogTitleBar

from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.layout.Column import Column
from albow.layout.Row import Row


class TitledDialog(Dialog):

    TD_SIZE:  int = 300

    wrap_width = ThemeProperty('wrap_width')
    """
    The number of pixels at which we wrap the input text message
    """

    def __init__(self, title: str = 'Default Title', message: str = '',
                 okTxt: str = 'Ok', cancelTxt: str = 'Cancel', thirdButtTxt: str = None,
                 client=None, wrapWidth: int = 100, **kwds):

        super().__init__(client=client, width=TitledDialog.TD_SIZE, **kwds)

        self.logger: Logger = getLogger(__name__)
        self.title:  str    = title
        self.wrap_width     = wrapWidth

        dlgTitleBar: DialogTitleBar = DialogTitleBar(theTitle=title, width=TitledDialog.TD_SIZE)
        lblMsg:      Label          = wrapped_label(message, self.wrap_width, margin=3, border_width=1, border_color=Theme.ELECTRON_BLUE)
        margin:      int            = self.margin
        self.logger.info(f'margin: {margin}')

        butOk:     Button = Button(okTxt,     action=lambda x=okTxt:     self.dismiss(x))
        butCancel: Button = Button(cancelTxt, action=lambda x=cancelTxt: self.dismiss(x))
        butThree:  Button = cast(Button, None)
        if thirdButtTxt is not None:
            butThree = Button(thirdButtTxt, action=lambda x=thirdButtTxt: self.dismiss(x))

        buttRowAttrs = {
            'spacing': margin,
            'margin': 4,
            'equalize': 'w',
            'border_width': 1,
            'border_color': Theme.ELECTRON_BLUE
        }
        if butThree is None:
            buttRow: Row = Row([butOk, butCancel], **buttRowAttrs)
        else:
            buttRow: Row = Row([butOk, butCancel, butThree], **buttRowAttrs)

        bottColAttrs = {
            'spacing': margin,
            'margin': 4,
            'align': 'r'
        }
        botColumn: Column = Column([lblMsg, buttRow], **bottColAttrs)

        mainColAttrs = {
            'align': 'l',
            'expand': 1,
            'margin': 8,
            'border_width':  2,
            'border_color': Theme.CITY_LIGHTS,
            'equalize': 'w'
        }
        mainColumn: Column = Column([dlgTitleBar, botColumn], **mainColAttrs)
        mainColumn.topleft = (margin, margin)

        self.add(mainColumn)
        self.shrink_wrap()
