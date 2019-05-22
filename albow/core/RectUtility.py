
class RectUtility:

    @staticmethod
    def rect_property(name):
        def get(self):
            return getattr(self._rect, name)

        def set(self, value):
            r = self._rect
            old_size = r.size
            setattr(r, name, value)
            new_size = r.size
            #
            # Python 3 update
            # i f old_size <> new_size:
            if old_size != new_size:
                #
                # Method signature changed since tuples not allowed to be passed
                #
                # self._resized(old_size)
                self._resized(old_size[0], old_size[1])

        return property(get, set)
