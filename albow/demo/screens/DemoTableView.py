
from albow.table.TableView import TableView
from albow.table.TableColumn import TableColumn


class DemoTableView(TableView):

    demo_table_data = [
        (1979, 12.5),
        (1980, 13.2),
        (1981, 13.5),
        (1982, 13.1),
        (1983, 14.3),
        (1984, 15.4),
        (1985, 16.4),
        (1986, 17.4),
        (1987, 18.4),
        (1988, 19.4),
        (2019, 23.0)
    ]

    selected_table_row = None

    columns = [
        TableColumn("Year", 70),
        TableColumn("Amount", 50, 'r', "%.1f"),
    ]

    def num_rows(self):
        return len(self.demo_table_data)

    def row_data(self, i):
        return self.demo_table_data[i]

    def row_is_selected(self, i):
        return self.selected_table_row == i

    def click_row(self, i, e):
        # global selected_table_row
        self.selected_table_row = i
