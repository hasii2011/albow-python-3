
from albow.dialog.Modal import Modal
from albow.widgets.Button import Button

from widget import Widget
from albow.layout.Row import Row
from albow.layout.Column import Column



class Dialog(Modal, Widget):

    click_outside_response = None

    def __init__(self, client = None, responses = None, default = 0, cancel = -1, **kwds):

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
                    Button(text, action = lambda t=text: self.dismiss(t))
                    for text in responses], equalize = 'w')
                rows.append(buttons)
                w2 = buttons.width
            if w1 < w2:
                a = 'l'
            else:
                a = 'r'
            contents = Column(rows, align = a)
            m = self.margin
            contents.topleft = (m, m)
            self.add(contents)
            self.shrink_wrap()
        if responses and default is not None:
            self.enter_response = responses[default]
        if responses and cancel is not None:
            self.cancel_response = responses[cancel]

    def mouse_down(self, e):
        if not e in self:
            response = self.click_outside_response
            if response is not None:
                self.dismiss(response)
