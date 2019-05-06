
from albow.dialog.Modal import Modal
from albow.widgets.Button import Button

from albow.core.Widget import Widget
from albow.layout.Row import Row
from albow.layout.Column import Column


class Dialog(Modal, Widget):
    """
    The Dialog class provides a convenient container for implementing modal dialogs. Pressing Return or
    Enter dismisses the dialog with the value True, and pressing Escape dismisses it with the value False.

    See the `albow.core.Widget` ``dismiss()`` and ``present()`` methods
    """
    click_outside_response = None
    """
    If this attribute is given a non-None value, then a mouse-down event outside the bounds of the dialog will 
    cause it to be dismissed with the given value.
    """
    def __init__(self, client=None, responses=None, default=0, cancel=-1, **kwds):
        """

        Args:
            client:    The widget the dialog is on top of

            responses: A list of responses

            default:   The index to the default response; Default is the first

            cancel:    The index to the cancel response; Default is None

            **kwds:
        """

        Widget.__init__(self, **kwds)
        if client or responses:
            rows = []
            w1 = 0
            w2 = 0
            if client:
                rows.append(client)
                w1 = client.width
            if responses:
                buttons = Row([
                    Button(text, action=lambda t=text: self.dismiss(t))
                    for text in responses], equalize='w')
                rows.append(buttons)
                w2 = buttons.width
            if w1 < w2:
                a = 'l'
            else:
                a = 'r'
            contents = Column(rows, align=a)
            m = self.margin
            contents.topleft = (m, m)
            self.add(contents)
            self.shrink_wrap()
        #
        # TODO  Appears to be some code for future use to provide other than True/False responses
        #
        if responses and default is not None:
            self.enter_response = responses[default]
        if responses and cancel is not None:
            self.cancel_response = responses[cancel]

    def mouse_down(self, e):
        #
        # PEP 8 update
        # https://lintlyci.github.io/Flake8Rules/rules/E713.html
        #
        # if not e in self:
        if e not in self:
            response = self.click_outside_response
            if response is not None:
                self.dismiss(response)
