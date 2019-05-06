import textwrap

from albow.widgets.Button import Button
from albow.widgets.Label import Label

from albow.dialog.Dialog import Dialog

from albow.layout.Row import Row
from albow.layout.Column import Column
from albow.input.TextField import TextField

DEFAULT_ASK_RESPONSES = ["OK", "Cancel"]


def wrapped_label(text, wrap_width, **kwds) -> Label:
    """
    Constructs a `albow.widgets.Label` widget from the given text after using the ``textwrap`` module to wrap it to
    the specified width in
    characters.
    Additional keyword parameters are passed to the Label constructor.

    Args:
        text:       The text to wrap in a label

        wrap_width: The wrap width

        **kwds:     Pass these to the Label constructor

    Returns:    A Label widget

    """
    paras = text.split("\n\n")
    text = "\n".join([textwrap.fill(para, wrap_width) for para in paras])
    return Label(text, **kwds)


def alert(theMessage: str, theWrapWidth=60, **kwds):
    """
    Displays a message in a modal dialog, wrapped to the specified width in characters. The dialog can be dismissed by
    pressing Return, Enter or Escape.

    Args:
        theMessage:  The alert message to display

        theWrapWidth:  The wrap width in characters

        **kwds: Additional keyword parameters passed to the `albow.dialog.Dialog` constructor.
    """
    ask(theMessage, ["OK"], wrap_width=theWrapWidth, **kwds)


def ask(theMessage: str, theResponses=None, default=0, cancel=-1, wrap_width=60, **kwds):
    """
    Displays a message in a modal dialog with a set of buttons labelled with the specified responses. Clicking a
    button causes the ask function to return the corresponding response string as its value. The default and
    cancel parameters are indexes into the response list specifying the values to be returned by Return/Enter
    and Escape, respectively.

    Args:
        theMessage: The message to display

        theResponses:  Possible responses

        default:  The index to the default message

        cancel: The index to the cancel message

        wrap_width:  The wrap width in characters

        **kwds: Additional keyword parameters passed to the Dialog constructor.

    Returns:    The dialog modal result

    """

    #
    # Fix 'Mutable default arguments'
    #
    if theResponses is None:
        theResponses = DEFAULT_ASK_RESPONSES
    box = Dialog(**kwds)
    d = box.margin
    lb = wrapped_label(theMessage, wrap_width)
    lb.topleft = (d, d)
    buts = []
    for caption in theResponses:
        but = Button(caption, action=lambda x=caption: box.dismiss(x))
        buts.append(but)
    brow = Row(buts, spacing=d, equalize='w')
    lb.width = max(lb.width, brow.width)
    col = Column([lb, brow], spacing=d, align='r')
    col.topleft = (d, d)
    if default is not None:
        box.enter_response = theResponses[default]
    else:
        box.enter_response = None
    if cancel is not None:
        box.cancel_response = theResponses[cancel]
    else:
        box.cancel_response = None
    box.add(col)
    box.shrink_wrap()

    return box.present()


def input_text(thePrompt: str, theInputWidth: int, theDefaultInput: str=None, **kwds):

    """
    Presents a modal dialog containing the given prompt and a text field. The theInputWidth is the width of
    the text field, and the theDefaultInput, if any, is its initial contents. If the dialog is dismissed by pressing
    Return or Enter, the contents of the text field is returned. If it is dismissed by pressing Escape, None
    is returned.

    Args:
        thePrompt:      The message to prompt with

        theInputWidth:  The width of the input text widget

        theDefaultInput: A possible default input

        **kwds:  Additional keyword parameters passed to the Dialog constructor.

    Returns:  The value that the user input
    """
    box = Dialog(**kwds)
    d = box.margin

    def ok():
        box.dismiss(True)

    def cancel():
        box.dismiss(False)

    lb = Label(thePrompt)
    lb.topleft = (d, d)
    tf = TextField(theInputWidth)
    if theDefaultInput:
        tf.set_text(theDefaultInput)
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
