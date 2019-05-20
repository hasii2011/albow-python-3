
from albow.containers.TabPanel import TabPanel
from albow.core.Widget import Widget
from albow.core.Shell import Shell

from albow.widgets.Label import Label

from albow.layout.Column import Column

from albow.demo.screens.BaseDemoScreen import BaseDemoScreen


class DemoTabPanelScreen(BaseDemoScreen):
    """

    """
    def __init__(self, shell: Shell):
        """

        :param shell:
        """
        #
        # Python 3 update
        #
        super().__init__(shell)
        tabPanel = TabPanel()
        tabPanel.size = 400, 200
        self.pages = tabPanel
        #
        # Python 3 update
        # for i in xrange(1, 4):
        for i in range(1, 4):
            page = self.make_test_page(i)
            tabPanel.add_page("Page %s" % i, page)

        contents = Column([tabPanel, self.backButton], spacing=BaseDemoScreen.DEFAULT_CONTENT_SPACING)
        self.add_centered(contents)

    def make_test_page(self, pageNumber: int) -> Widget:
        """

        :param pageNumber: Guess :-)

        :return:  The widget page
        """
        page_size = self.pages.content_size()
        page = Widget(size=page_size, border_width = 1)
        lbl = Label(f"This is page {pageNumber}")
        page.add_centered(lbl)

        return page
