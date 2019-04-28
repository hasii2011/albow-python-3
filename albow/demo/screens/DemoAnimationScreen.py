
import random

from albow.core.screen import Screen
from albow.shell import Shell

from albow.widgets.Button import Button


class DemoAnimationScreen(Screen):
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

        btn = Button("Menu", action=self.go_back)
        btn.rect.center = (w/2, h - 20)
        self.add(btn)

    def draw(self, surface):
        from pygame.draw import polygon
        polygon(surface, (128, 200, 255), self.points)
        polygon(surface, (255, 128, 0), self.points, 5)

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

    def go_back(self):
        self.parent.show_menu()
