
import textwrap

from albow.widgets.Label import Label


def wrapped_label(text: str, wrap_width: int, **kwds) -> Label:
    """
    Constructs a `albow.widgets.Label` widget from the given text after using the ``textwrap`` module to wrap it to
    the specified width in characters.

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

