
import logging

from albow.themes.Theme import Theme
from albow.core.ui.Widget import Widget

class Predictor:

    def __init__(self, theWidget: Widget):

        self.logger = logging.getLogger(__name__)
        self.widget = theWidget

    def predict(self, kwds, name):
        try:
            return kwds[name]
        except KeyError:
            return Theme.getThemeRoot().get(self.widget.__class__, name)

    def predict_attr(self, kwds, name):
        try:
            return kwds[name]
        except KeyError:
            return getattr(self.widget, name)

    def init_attr(self, kwds, name):
        try:
            return kwds.pop(name)
        except KeyError:
            return getattr(self.widget, name)

    def predict_font(self, kwds, name='font'):
        return kwds.get(name) or Theme.getThemeRoot().get_font(self.widget.__class__, name)

