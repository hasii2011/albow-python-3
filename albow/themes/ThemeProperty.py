
import sys

import logging

from albow.themes.Theme import root

debug_theme = False


class ThemeProperty:

    def __init__(self, name):
        """

        :param name:
        """

        self.logger = logging.getLogger(__name__)
        self.name = name
        self.cache_name = sys.intern("_" + name)

    def __get__(self, obj, owner):
        """
        TODO use python logging instead of print

        :param obj:
        :param owner:
        :return:
        """
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
                # if debug_theme:
                #     print(e)
                self.logger.exception("Attribute error: %s", e)
                value = self.get_from_theme(obj.__class__, self.name)
                obj.__dict__[cache_name] = value
                return value
        #
        # TODO Do not use bare exception
        #
        except:
            if debug_theme:
                import traceback
                traceback.print_exc()
                print("-------------------------------------------------------")
            raise

    def __set__(self, obj, value):
        """

        :param obj:
        :param value:
        :return:
        """
        self.logger.debug("Setting %s.%s = %s", obj, self.cache_name, value)
        obj.__dict__[self.cache_name] = value

    def get_from_theme(self, cls, name):
        return root.get(cls, name)
