
import random

from albow.core.ui.Widget import Widget

POLYGON_BORDER_WIDTH: int = 2


class DemoAnimationWidget(Widget):
    def __init__(self, parent, **attrs):

        super().__init__(**attrs)

        self.rect = parent.rect.inflate(-100, -100)
        w, h = self.size
        self.points = [[100, 50], [w - 50, 100], [50, h - 50]]

        def randomValue():
            return random.randint(-5, 5)

        self.velocities = [
            [randomValue(), randomValue()] for i in range(len(self.points))
        ]

    def draw(self, surface):
        from pygame.draw import polygon
        polygon(surface, (128, 200, 255), self.points)
        polygon(surface, (255, 128, 0),   self.points, POLYGON_BORDER_WIDTH)
        self.animate()

    def animate(self):
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
