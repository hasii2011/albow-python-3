
class Page:

    def __init__(self, text_screen, heading, lines):
        """

        Args:
            text_screen:
            heading:
            lines:
        """
        self.text_screen = text_screen
        self.heading = heading
        self.lines = lines
        width, height = text_screen.heading_font.size(heading)
        for line in lines:
            w, h = text_screen.font.size(line)
            width = max(width, w)
            height += h
        self.size = (width, height)

    def draw(self, surface, color, pos):
        """

        Args:
            surface:
            color:
            pos:

        Returns:

        """
        heading_font = self.text_screen.heading_font
        text_font = self.text_screen.font
        x, y = pos
        buf = heading_font.render(self.heading, True, color)
        surface.blit(buf, (x, y))
        y += buf.get_rect().height
        for line in self.lines:
            buf = text_font.render(line, True, color)
            surface.blit(buf, (x, y))
            y += buf.get_rect().height
