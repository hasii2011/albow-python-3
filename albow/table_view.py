"""
	Albow - Table View
"""

from pygame import Rect
from albow.layouts.Column import Column
from palette_view import PaletteView
from utils import blit_in_rect


class TableView(Column):

	columns = []
	header_font = None
	header_fg_color = None
	header_bg_color = None
	header_spacing = 5
	column_margin = 2
	
	def __init__(self, nrows=None, height=None, header_height=None, row_height=None, scrolling=True, **kwds):
		"""

		:param nrows:
		:param height:
		:param header_height:
		:param row_height:
		:param scrolling:
		:param kwds:
		"""
		columns = self.predict_attr(kwds, 'columns')
		if row_height is None:
			font = self.predict_font(kwds)
			row_height = font.get_linesize()
		if header_height is None:
			header_height = row_height
		row_width = 0
		if columns:
			for column in columns:
				row_width += column.width
			row_width += 2 * self.column_margin * len(columns)
		contents = []
		header = None
		if header_height:
			header = TableHeaderView(row_width, header_height)
			contents.append(header)
		row_size = (row_width, row_height)
		if not nrows and height:
			nrows = height // row_height
		rows = TableRowView(row_size, nrows or 10, scrolling=scrolling)
		contents.append(rows)
		s = self.header_spacing
		#
		# Python 3 update
		#
		# Column.__init__(self, contents, align = 'l', spacing = s, **kwds)
		super().__init__(contents, align='l', spacing=s, **kwds)
		if header:
			header.font     = self.header_font or self.font
			header.fg_color = fg_color = self.header_fg_color or self.fg_color
			header.bg_color = bg_color = self.header_bg_color or self.bg_color
		rows.font = self.font
		rows.fg_color  = self.fg_color
		rows.bg_color  = self.bg_color
		rows.sel_color = self.sel_color
	
	def column_info(self, row_data):
		columns = self.columns
		m = self.column_margin
		d = 2 * m
		x = 0
		for i, column in enumerate(columns):
			width = column.width
			if row_data:
				data = row_data[i]
			else:
				data = None
			yield i, x + m, width - d, column, data
			x += width
	
	def draw_header_cell(self, surf, i, cell_rect, column):
		self.draw_text_cell(surf, i, column.title, cell_rect,
			column.alignment, self.font)

	def draw_table_cell(self, surf, i, data, cell_rect, column):
		text = column.format(data)
		self.draw_text_cell(surf, i, text, cell_rect, column.alignment, self.font)

	def draw_text_cell(self, surf, i, data, cell_rect, align, font):
		buf = font.render(str(data), True, self.fg_color)
		blit_in_rect(surf, buf, cell_rect, align)
	
	def row_is_selected(self, n):
		return False
	
	def click_row(self, n, e):
		pass


class TableColumn(object):
	#  title           string
	#  width           int
	#  alignment       'l' or 'c' or 'r'
	#  formatter       func(data) -> string
	#  format_string   string                Used by default formatter
	
	format_string = "%s"
	
	def __init__(self, title, width, align = 'l', fmt = None):
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


class TableRowBase(PaletteView):

	def __init__(self, cell_size, nrows, scrolling, **kwds):
		"""

		:param cell_size:
		:param nrows:
		:param scrolling:
		"""
		#
		# Python 3 update
		#
		# PaletteView.__init__(self, cell_size, nrows, 1, scrolling=scrolling)
		super().__init__(cell_size, nrows, 1, scrolling=scrolling, **kwds)
	
	def num_items(self):
		return self.parent.num_rows()
	
	def draw_item(self, surf, row, row_rect):
		table = self.parent
		height = row_rect.height
		row_data = self.row_data(row)
		for i, x, width, column, cell_data in table.column_info(row_data):
			cell_rect = Rect(x, row_rect.top, width, height)
			self.draw_table_cell(surf, i, cell_data, cell_rect, column)
	
	def row_data(self, row):
		return self.parent.row_data(row)

	def draw_table_cell(self, surf, i, data, cell_rect, column):
		self.parent.draw_table_cell(surf, i, data, cell_rect, column)


class TableRowView(TableRowBase):

	highlight_style = 'fill'
	vstretch = True

	#
	# Python 3 update to make sure scrolling values get passed through
	#
	def __init__(self, cellSize: int, nRows: int, scrolling: bool):
		super().__init__(cellSize, nRows, scrolling)

	def item_is_selected(self, n):
		return self.parent.row_is_selected(n)

	def click_item(self, n, e):
		self.parent.click_row(n, e)


class TableHeaderView(TableRowBase):

	def __init__(self, width, height):
		TableRowBase.__init__(self, (width, height), 1, False)

#	def row_data(self, row):
#		return [c.title for c in self.parent.columns]
	
#	def draw_table_cell(self, surf, i, text, cell_rect, column):
#		self.parent.draw_header_cell(surf, i, text, cell_rect, column)

	def row_data(self, row):
		pass
			
	def draw_table_cell(self, surf, i, data, cell_rect, column):
		self.parent.draw_header_cell(surf, i, cell_rect, column)
