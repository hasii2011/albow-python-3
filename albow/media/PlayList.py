
from random import randrange


class PlayList:
    """
    A collection of music filenames to be played sequentially or
    randomly. If random is true, items will be played in a random order.
    If repeat is true, the list will be repeated indefinitely, otherwise
    each item will only be played once.
    """

    random: bool = None
    """
    If true, items will be played in a random order. Otherwise, they will be played in the order they were supplied 
    to the constructor.
    """
    repeat: bool = None
    """
    If true, the list will be repeated indefinitely. Otherwise, each item will only be played once.
    """

    def __init__(self, items, random: bool=False, repeat: bool=False):
        """
        Constructs a PlayList from a list of music file pathnames.

        Args:
            items:  Music file pathnames

            random: The new random state

            repeat: The new repeat state
        """
        self.items = list(items)
        self.random = random
        self.repeat = repeat

    def next(self):
        """
        Returns the next item to be played.
        """
        items = self.items
        if items:
            if self.random:
                n = len(items)
                if self.repeat:
                    n = (n + 1) // 2
                i = randrange(n)
            else:
                i = 0
            item = items.pop(i)
            if self.repeat:
                items.append(item)
            return item
