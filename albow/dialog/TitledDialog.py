
from logging import Logger
from logging import getLogger

# from pygame import Surface
# from pygame import Rect
#
from albow.themes.Theme import Theme

from albow.themes.ThemeProperty import ThemeProperty

from albow.dialog.DialogUtilities import wrapped_label
from albow.dialog.Dialog import Dialog
from albow.dialog.DialogTitleBar import DialogTitleBar

from albow.widgets.Button import Button

from albow.layout.Column import Column
from albow.layout.Row import Row


class TitledDialog(Dialog):

    TD_SIZE:  int = 300

    wrap_width = ThemeProperty('wrap_width')
    """
    The number of pixels at which we wrap the input text message
    """

    def __init__(self, title: str = 'Default Title', message: str = '', client=None, **kwds):

        super().__init__(client=client, width=TitledDialog.TD_SIZE, **kwds)

        self.logger: Logger = getLogger(__name__)
        self.title:  str    = title

        dlgTitleBar: DialogTitleBar = DialogTitleBar(theTitle=title, width=TitledDialog.TD_SIZE)
        lb     = wrapped_label(message, self.wrap_width)
        margin = self.margin
        self.logger.info(f'margin: {margin}')

        butOk:     Button = Button('Ok',     action=lambda x='Ok': self.dismiss(x))
        butCancel: Button = Button('Cancel', action=lambda x='Cancel': self.dismiss(x))

        brow     = Row([butOk, butCancel], spacing=margin, equalize='w')
        lb.width = max(lb.width, brow.width)

        col      = Column([dlgTitleBar, lb, brow], spacing=margin, align='r')
        col.topleft = (margin, margin)

        self.add(col)
        self.shrink_wrap()
