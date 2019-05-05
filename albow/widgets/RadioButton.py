
from albow.widgets.CheckWidget import CheckWidget
from albow.widgets.RadioControl import RadioControl


class RadioButton(RadioControl, CheckWidget):
    """
    RadioButton controls are intended to be used in a group to provide a multiple-choice selection. To achieve t
    his, all the radio buttons in the group should be linked via their ref attributes to the same value, and each
    one given a unique setting. The one whose setting matches the current value displays its check mark, and
    clicking on a radio button sets the value to that button's setting.

    Note that a RadioButton does not have a title; you will need to place a Label beside it if you want one.

    The visual appearance of a RadioButton is currently the same as a CheckBox. This may change in a later version.
    """
    pass
