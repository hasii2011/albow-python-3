
import sys

import logging

from albow.themes.Theme import Theme


class ThemeProperty:
    """
    The ThemeProperty class is a property descriptor used for defining theme properties.

    Example
    --------
    ```python

        class Battlefield(Widget):

        phaser_color = ThemeProperty('phaser_color')

    ```
    """
    debug_theme = False

    def __init__(self, name):
        """
        Constructs a theme property. The name given is used to derive the name under which the
        property value is cached, by pre-pending an underscore. Normally name should be the same as
        the name being used for the property.

        Args:
            name:   The property name
        """
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.cache_name = sys.intern("_" + name)

    def __get__(self, obj, owner):
        self.logger.debug("%s(%s).__get__(%s)", self.__class__.__name__, self.name, obj)

        try:
            cache_name = self.cache_name
            try:
                return getattr(obj, cache_name)
            #
            # Python 3 update
            #
            # except AttributeError, e:
            except AttributeError as e:
                if ThemeProperty.debug_theme:
                    self.logger.exception(f"{e}.  Ok. Get value from Theme")
                value = self.get_from_theme(obj.__class__, self.name)
                obj.__dict__[cache_name] = value
                return value
        #
        # TODO Do not use bare exception
        #
        except:
            if ThemeProperty.debug_theme:
                import traceback
                traceback.print_exc()
                self.logger.debug("-------------------------------------------------------")
            raise

    def __set__(self, obj, value):
        """

        Args:
            obj:

            value:

        Returns:

        """
        self.logger.debug(f"Setting {obj}.{self.cache_name} = {value}")
        obj.__dict__[self.cache_name] = value

    def get_from_theme(self, cls, name):
        return Theme.getThemeRoot().get(cls, name)
