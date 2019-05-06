
class Modal:
    """
    Modal is a mixin class for use by widgets that define modal states. It provides default responses for the Enter
    and Escape keys and methods that can be used as actions for OK and Cancel buttons.
    """
    enter_response = True
    """
    Value with which to dismiss a modal dialog when the Return or Enter key is pressed.
    """
    cancel_response = False
    """
    Value with which to dismiss a modal dialog when the Escape key is pressed.
    """

    # These aren't used because subclasses of Modal seem to be using
    # Widget.dismiss()
    #
    # def ok(self):
    #     self.dismiss(True)
    #
    # def cancel(self):
    #     self.dismiss(False)
