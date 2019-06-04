
import logging

from pygame.font import Font

import pygame


from albow.themes.Theme import Theme
from albow.themes.ThemeLoader import ThemeLoader

from albow.core.ui.Predictor import Predictor

from test.TestBase import TestBase

from test.DummyWidget import DummyWidget


class TestPredictor(TestBase):

    @classmethod
    def setUpClass(cls):
        """"""
        TestBase.setUpLogging()
        themeLoader: ThemeLoader = ThemeLoader()
        themeLoader.load()
        themeRoot: Theme = themeLoader.themeRoot
        Theme.setThemeRoot(themeRoot)

    def setUp(self):
        """"""
        self.logger = logging.getLogger(__name__)

    def testBasic(self):

        dummyWidget: DummyWidget = DummyWidget()
        predictor: Predictor = Predictor(dummyWidget)

        kwds = {
            'margin': 5
        }
        val = predictor.predict(kwds, 'margin')
        self.assertIsNotNone(val, "Something is broken")
        self.assertEqual(val, 5, "Predicted incorrectly")

        val = predictor.predict(kwds, 'bg_color')
        self.assertIsNotNone(val, "Should get it from widget")
        self.assertEqual(val, (208, 210, 211), "Got wrong value")

    def testBasicPredictAttr(self):

        dummyWidget: DummyWidget = DummyWidget()
        predictor: Predictor = Predictor(dummyWidget)

        kwds = {}
        val = predictor.predict_attr(kwds, 'is_modal')

        self.assertIsNotNone(val, "Should get it from widget")
        self.assertEqual(val, False, "Wrong value")

    def testBasicPredictFont(self):

        dummyWidget: DummyWidget = DummyWidget()
        predictor: Predictor = Predictor(dummyWidget)

        pygame.init()
        kwds = {}
        val: Font = predictor.predict_font(kwds)

        self.assertIsNotNone(val, "Should get it from widget")
