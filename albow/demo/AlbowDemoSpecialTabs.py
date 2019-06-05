
from albow.widgets.Label import Label

from albow.layout.Column import Column
from albow.layout.Row import Row

from albow.demo.screens.DemoUserEventsScreen import DemoUserEventsScreen

from albow.demo.ScheduledEventTabPage import ScheduledEventTabPage

from albow.demo.views.DemoTableView import DemoTableView
from albow.demo.views.DemoGridView import DemoGridView
from albow.demo.views.DemoPaletteView import DemoPaletteView


class AlbowDemoSpecialTabs:

    @classmethod
    def makeEventsTab(cls) -> Column:

        userEvents: Column = DemoUserEventsScreen.makeContents()
        scheduledEventsTabPage: ScheduledEventTabPage = ScheduledEventTabPage(height=userEvents.height, width=userEvents.width)
        contentAttrs = {
            'align': "c",
            'margin': 10
        }
        eventTab: Column = Column([userEvents, scheduledEventsTabPage], **contentAttrs)

        from albow.demo.AlbowDemoScreen import AlbowDemoScreen

        AlbowDemoScreen.classScheduledEventsTabPage = scheduledEventsTabPage
        return eventTab

    @classmethod
    def makeGridLikeTab(cls):

        gridTabAttrs = {
            'align': "c",
            'margin': 20
        }

        grid: DemoGridView = DemoGridView()
        lbl = Label("Cl1ck a Squ4r3")
        grid.output = lbl

        gridColumn: Column = Column([grid, lbl])

        table: DemoTableView = DemoTableView()
        palette: DemoPaletteView = DemoPaletteView()

        gridTab: Row = Row([table, palette, gridColumn], **gridTabAttrs)

        return gridTab
