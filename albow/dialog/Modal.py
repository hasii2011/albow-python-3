
class Modal(object):

    enter_response = True
    cancel_response = False

    # These aren't used because subclasses of Modal seem to be using
    # Widget.dismiss()
    #
    # def ok(self):
    #     self.dismiss(True)
    #
    # def cancel(self):
    #     self.dismiss(False)
