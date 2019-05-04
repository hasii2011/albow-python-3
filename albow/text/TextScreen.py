
from pygame.locals import *
from albow.core.Screen import Screen

from albow.themes.FontProperty import FontProperty

from albow.widgets.Button import Button
from albow.text.Page import Page

from albow.core.ResourceUtility import ResourceUtility

from albow.vectors import add
from albow.vectors import maximum


class TextScreen(Screen):

    bg_color = (0, 0, 0)
    fg_color = (255, 255, 255)
    border   = 20

    heading_font = FontProperty('heading_font')
    button_font  = FontProperty('button_font')

    def __init__(self, shell, filename, **kwds):
        """"""
        text = ResourceUtility.get_text(filename)
        text_pages = text.split("\nPAGE\n")
        pages = []
        page_size = (0, 0)
        for text_page in text_pages:
            lines = text_page.strip().split("\n")
            page  = Page(self, lines[0], lines[1:])
            pages.append(page)
            page_size = maximum(page_size, page.size)
        self.pages = pages
        bf = self.button_font
        b1 = Button("Prev Page", font=bf, action=self.prev_page)
        b2 = Button("Menu",      font=bf, action=self.go_back)
        b3 = Button("Next Page", font=bf, action=self.next_page)
        b  = self.margin
        # page_rect = Rect((b, b), page_size)
        width_height  = list(map(lambda x: x, page_size))

        page_rect = Rect((b, b),(width_height[0],width_height[1]))

        gap = (0, 18)
        #
        # Python 3 update
        #
        # In Python 3 maps and list are not auto-converted
        #
        # b1.topleft  = add(page_rect.bottomleft,  gap)
        # b2.midtop   = add(page_rect.midbottom,   gap)
        # b3.topright = add(page_rect.bottomright, gap)
        b1.topleft  = list(add(page_rect.bottomleft,  gap))
        b2.midtop   = list(add(page_rect.midbottom,   gap))
        b3.topright = list(add(page_rect.bottomright, gap))

        # Screen.__init__(self, shell, **kwds)
        super().__init__(shell, **kwds)
        #
        # Python 3 update
        #
        # In Python 3 maps and list are not auto-converted
        #
        # self.size =  add(b3.bottomright, (b, b))
        self.size = list(add(b3.bottomright, (b, b)))
        self.add(b1)
        self.add(b2)
        self.add(b3)
        self.prev_button = b1
        self.next_button = b3
        self.set_current_page(0)

    def draw(self, surface):
        b = self.margin
        self.pages[self.current_page].draw(surface, self.fg_color, (b, b))

    def at_first_page(self):
        return self.current_page == 0

    def at_last_page(self):
        return self.current_page == len(self.pages) - 1

    def set_current_page(self, n):
        self.current_page = n
        self.prev_button.enabled = not self.at_first_page()
        self.next_button.enabled = not self.at_last_page()

    def prev_page(self):
        if not self.at_first_page():
            self.set_current_page(self.current_page - 1)

    def next_page(self):
        if not self.at_last_page():
            self.set_current_page(self.current_page + 1)

    def go_back(self):
        self.parent.show_menu()
