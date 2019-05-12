
class ItemRefInsertionException(Exception):
    """
    This exception is thrown if there is a problem when updating an ItemRef
    object
    """
    def __init__(self, theIndex: int, theMessage:str =None):
        """

        Args:
            theIndex:  The index where the insertion error occurred

            theMessage: A custom message
        """
        self.index = theIndex

        if theMessage == None:
            self.message = f"Can't insert item at {theIndex}"
        else:
            self.message = f"{theMessage}: at index: {theIndex}"
