
import random

from albow.core.Shell import Shell

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen

POLYGON_BORDER_WIDTH: int = 2


class DemoAnimationScreen(BaseDemoScreen):
    """
    Animation
    """

    def __init__(self, shell: Shell):

        #
        # Python 3 update
        #
        super().__init__(shell)
        self.rect = shell.rect.inflate(-100, -100)
        w, h = self.size
        self.points = [[100, 50], [w - 50, 100], [50, h - 50]]

        def randomValue():
            return random.randint(-5, 5)

        self.velocities = [
            [randomValue(), randomValue()] for i in range(len(self.points))
        ]

        self.backButton.rect.center = (w/2, h - 20)

        self.add(self.backButton)

    def draw(self, surface):
        from pygame.draw import polygon
        polygon(surface, (128, 200, 255), self.points)
        polygon(surface, (255, 128, 0),   self.points, POLYGON_BORDER_WIDTH)

    def begin_frame(self):
        r = self.rect
        w, h = r.size
        for p, v in zip(self.points, self.velocities):
            p[0] += v[0]
            p[1] += v[1]
            if not 0 <= p[0] <= w:
                v[0] = -v[0]
            if not 0 <= p[1] <= h:
                v[1] = -v[1]
        self.invalidate()
