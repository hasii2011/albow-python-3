
from pygame import Rect
from albow.core.Widget import Widget
from albow.themes.ThemeProperty import ThemeProperty
from albow.themes.FontProperty import FontProperty

from albow.utils import brighten


class TabPanel(Widget):
    """
    A `TabPanel` is a widget that manages a collection of pages and displays one of them at a time. Switching
    between pages is accomplished by means of a row of 'tabs' at the top of the TabPanel, one for each page.
    Clicking on a tab brings its corresponding page to the front.
    """

    tab_font = FontProperty('tab_font')
    """
    Font in which to display the page titles in the tabs.
    """
    tab_height = ThemeProperty('tab_height')
    """
    Height of the tabs.
    """
    tab_border_width = ThemeProperty('tab_border_width')
    """
    Width of the border, if any, to draw around each tab.
    """
    tab_spacing = ThemeProperty('tab_spacing')
    """
    Width of space to leave between adjacent tabs.
    """
    tab_margin = ThemeProperty('tab_margin')
    """
    Width of space to leave before the first tab and after the last tab.
    """
    tab_fg_color = ThemeProperty('tab_fg_color')
    """
    Color in which to display the page titles.
    """
    default_tab_bg_color = ThemeProperty('default_tab_bg_color')
    """
    Color with which to fill the background of any tab whose page does not specify a tab color.
    """
    tab_area_bg_color = ThemeProperty('tab_area_bg_color')
    """
    Color with which to fill any background areas of the tab region not covered by a tab.
    """
    tab_dimming = ThemeProperty('tab_dimming')
    """
    Factor by which to dim the background colour of tabs other than the currently selected tab. The range is 
    0.0 to 1.0.
    """

    def __init__(self, pages=None, **kwds):
        """

        Args:
            pages:  The pages, if provided should be a sequence of (title, widget) pairs, which will
                    be added by the add_page() method.

            **kwds:
        """
        #
        # Python 3 update
        #
        super().__init__(**kwds)
        self.pages = []
        self.current_page = None
        if pages:
            w = h = 0
            for title, page in pages:
                w = max(w, page.width)
                h = max(h, page.height)
                self._add_page(title, page)
            self.size = (w, h)
            self.show_page(pages[0][1])

    def content_size(self) -> tuple:
        """
        The area that a page will take up when it is displayed.

        Returns:  A tuple `(width, height)` of the size of the content area
        """
        return self.width, self.height - self.tab_height

    def content_rect(self) -> Rect:
        """

        Returns:  A `Rect` representing the content area in the local coordinate system of the `TabPanel`.
        """
        return Rect((0, self.tab_height), self.content_size())

    def page_height(self) -> int:
        """

        Returns:  The height of a page (equal to the height of the content_rect()).

        """
        return self.height - self.tab_height

    def add_page(self, theTitle: str, thePage: Widget):
        """
        Adds the given widget as a new page, with the specified title to be displayed in its tab.

        .. Note::
            The widget should **NOT** also be added using add(); the TabPanel will do that itself when appropriate.

        Args:
            theTitle:   The page title

            thePage:    The widget that is the page

        """
        self._add_page(theTitle, thePage)
        if not self.current_page:
            self.show_page(thePage)

    def _add_page(self, title, page):
        page.tab_title = title
        page.anchor = 'ltrb'
        self.pages.append(page)

    def remove_page(self, thePage: Widget):
        """
        Removes the specified page, if present.

        Args:
            thePage:  The page to remove

        """
        try:
            i = self.pages.index(thePage)
            del self.pages[i]
        except IndexError:
            pass
        if thePage is self.current_page:
            self.show_page(None)

    def show_page(self, page):
        if self.current_page:
            self.remove(self.current_page)
        self.current_page = page
        if page:
            th = self.tab_height
            page.rect = Rect(0, th, self.width, self.height - th)
            self.add(page)
            page.focus()

    def draw(self, surf):
        self.draw_tab_area_bg(surf)
        self.draw_tabs(surf)

    def draw_tab_area_bg(self, surf):
        bg = self.tab_area_bg_color
        if bg:
            surf.fill(bg, (0, 0, self.width, self.tab_height))

    def draw_tabs(self, surf):
        font = self.tab_font
        fg = self.tab_fg_color
        b = self.tab_border_width
        if b:
            surf.fill(fg, (0, self.tab_height - b, self.width, b))
        for i, title, page, selected, rect in self.iter_tabs():
            x0 = rect.left
            w = rect.width
            h = rect.height
            r = rect
            if not selected:
                r = Rect(r)
                r.bottom -= b
            self.draw_tab_bg(surf, page, selected, r)
            if b:
                surf.fill(fg, (x0, 0, b, h))
                surf.fill(fg, (x0 + b, 0, w - 2 * b, b))
                surf.fill(fg, (x0 + w - b, 0, b, h))
            buf = font.render(title, True, page.fg_color or fg)
            r = buf.get_rect()
            r.center = (x0 + w // 2, h // 2)
            surf.blit(buf, r)

    def iter_tabs(self):
        pages = self.pages
        current_page = self.current_page
        n = len(pages)
        b = self.tab_border_width
        s = self.tab_spacing
        h = self.tab_height
        m = self.tab_margin
        width = self.width - 2 * m + s - b
        x0 = m
        for i, page in enumerate(pages):
            x1 = m + (i + 1) * width // n
            selected = page is current_page
            yield i, page.tab_title, page, selected, Rect(x0, 0, x1 - x0 - s + b, h)
            x0 = x1

    def draw_tab_bg(self, surf, page, selected, rect):
        bg = self.tab_bg_color_for_page(page)
        if not selected:
            bg = brighten(bg, self.tab_dimming)
        surf.fill(bg, rect)

    def tab_bg_color_for_page(self, page):
        return getattr(page, 'tab_bg_color', None) \
            or page.bg_color \
            or self.default_tab_bg_color

    def mouse_down(self, e):
        x, y = e.local
        if y < self.tab_height:
            i = self.tab_number_containing_x(x)
            if i is not None:
                self.show_page(self.pages[i])

    def tab_number_containing_x(self, x):
        n = len(self.pages)
        m = self.tab_margin
        width = self.width - 2 * m + self.tab_spacing - self.tab_border_width
        i = (x - m) * n // width
        if 0 <= i < n:
            return i
