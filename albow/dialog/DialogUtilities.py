import textwrap

from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.dialog.Dialog import Dialog

from albow.layout.Row import Row
from albow.layout.Column import Column
from fields import TextField


def wrapped_label(text, wrap_width, **kwds):

    paras = text.split("\n\n")
    text = "\n".join([textwrap.fill(para, wrap_width) for para in paras])
    return Label(text, **kwds)


def alert(mess, **kwds):
    ask(mess, ["OK"], **kwds)


def ask(mess, responses=["OK", "Cancel"], default=0, cancel=-1, wrap_width=60, **kwds):
    """

    :param mess:
    :param responses: This is a mutable default parameter;  TODO Fix this
    :param default:
    :param cancel:
    :param wrap_width:
    :param kwds:
    :return:
    """
    box = Dialog(**kwds)
    d = box.margin
    lb = wrapped_label(mess, wrap_width)
    lb.topleft = (d, d)
    buts = []
    for caption in responses:
        but = Button(caption, action=lambda x=caption: box.dismiss(x))
        buts.append(but)
    brow = Row(buts, spacing=d, equalize='w')
    lb.width = max(lb.width, brow.width)
    col = Column([lb, brow], spacing=d, align='r')
    col.topleft = (d, d)
    if default is not None:
        box.enter_response = responses[default]
    else:
        box.enter_response = None
    if cancel is not None:
        box.cancel_response = responses[cancel]
    else:
        box.cancel_response = None
    box.add(col)
    box.shrink_wrap()
    return box.present()


def input_text(prompt, width, initial=None, **kwds):

    box = Dialog(**kwds)
    d = box.margin

    def ok():
        box.dismiss(True)

    def cancel():
        box.dismiss(False)

    lb = Label(prompt)
    lb.topleft = (d, d)
    tf = TextField(width)
    if initial:
        tf.set_text(initial)
    tf.enter_action = ok
    tf.escape_action = cancel
    tf.top = lb.top
    tf.left = lb.right + 5
    box.add(lb)
    box.add(tf)
    tf.focus()
    box.shrink_wrap()
    if box.present():
        return tf.get_text()
    else:
        return None
