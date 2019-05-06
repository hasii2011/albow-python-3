
class TableColumn:

    format_string = "%s"

    def __init__(self, title: str, width: int, align: str = 'l', fmt: str = None):
        """

        Args:
            title:
            width:
            align:
            fmt:
        """
        self.title = title
        self.width = width
        self.alignment = align
        if fmt:
            #
            # Python 3 everything is unicode  -- hasii
            #
            # if isinstance(fmt, (str, unicode)):
            # 	self.format_string = fmt
            # else:
            # 	self.formatter = fmt
            self.format_string = fmt

    def format(self, data):
        if data is not None:
            return self.formatter(data)
        else:
            return ""

    def formatter(self, data):
        return self.format_string % data
