
from albow.core.ApplicationException import ApplicationException


class CancelException(ApplicationException):
    """
    Raising CancelException causes control to be returned silently to the event loop. It can be used to cancel
    an operation, for example in response to cancelling a modal dialog.
    """
    pass
