#-----------------------------------------------------------------------
#
#   Albow - Multiple-choice controls
#
#-----------------------------------------------------------------------

from controls import Control
from palette_view import PaletteView
from albow.utils import blit_in_rect
from theme import ThemeProperty
from pygame import draw
from pygame.locals import K_LEFT, K_RIGHT

#-----------------------------------------------------------------------

class Multichoice(PaletteView, Control):

	highlight_color = ThemeProperty('highlight_color')
	cell_margin = ThemeProperty('cell_margin')

	#highlight_style = 'frame'
	align = 'c'
	tab_stop = True

	def __init__(self, cell_size, values, **kwds):
		PaletteView.__init__(self, cell_size, 1, len(values), **kwds)
		self.values = values

	def num_items(self):
		return len(self.values)
	
	def item_is_selected(self, n):
		return self.get_value() == self.values[n]
	
	def click_item(self, n, e):
		if self.tab_stop:
			self.focus()
		self.set_value(self.values[n])
	
	def draw(self, surf):
		if self.has_focus():
			surf.fill(self.highlight_color)
		PaletteView.draw(self, surf)

	def key_down(self, e):
		k = e.key
		if k == K_LEFT:
			self.change_value(-1)
		elif k == K_RIGHT:
			self.change_value(1)
		else:
			PaletteView.key_down(self, e)
	
	def change_value(self, d):
		values = self.values
		if values:
			n = len(values)
			value = self.get_value()
			try:
				i = values.index(value)
			except ValueError:
				if d < 0:
					i = 0
				else:
					i = n - 1
			else:
				i = max(0, min(n - 1, i + d))
			self.set_value(values[i])

#-----------------------------------------------------------------------

class TextMultichoice(Multichoice):

	def __init__(self, values, labels = None, **kwds):
		if not labels:
			labels = map(str, values)
		font = self.predict_font(kwds)
		d = 2 * self.predict(kwds, 'margin')
		cd = 2 * self.predict(kwds, 'cell_margin')
		wmax = hmax = 0
		for (w, h) in map(font.size, labels):
			wmax = max(wmax, w)
			hmax = max(hmax, h)
		cw = wmax + cd
		ch = hmax + cd
		Multichoice.__init__(self, (cw, ch), values, **kwds)
		self.labels = labels

	def draw_item(self, surf, n, rect):
		buf = self.font.render(self.labels[n], True, self.fg_color)
		blit_in_rect(surf, buf, rect, self.align, self.margin)

	def draw_prehighlight(self, surf, i, rect):
		if self.highlight_style == 'arrows':
			self.draw_arrows(surf, i, rect)
		else:
			Multichoice.draw_prehighlight(self, surf, i, rect)

	def draw_arrows(self, surf, i, rect):
		m = self.margin
		color = self.sel_color or self.fg_color
		x, y = rect.midtop
		pts = [(x - m, y - m), (x + m, y - m), (x, y)]
		draw.polygon(surf, color, pts)
		x, y = rect.midbottom
		y -= 1
		pts = [(x - m, y + m), (x + m, y + m), (x, y)]
		draw.polygon(surf, color, pts)
	
#-----------------------------------------------------------------------

class ImageMultichoice(Multichoice):

	highlight_style = 'fill'
	sel_color = (255, 192, 19)
	margin = 5

	def __init__(self, images, values, **kwds):
		image0 = images[0]
		w, h = image0.get_size()
		d = 2 * self.predict(kwds, 'margin')
		cell_size = w + d, h + d
		Multichoice.__init__(self, cell_size, values, **kwds)
		self.images = images

	def draw_item(self, surf, n, rect):
		image = self.images[n]
		blit_in_rect(surf, image, rect, self.align, self.margin)
	
	def draw_prehighlight(self, surf, i, rect):
		color = self.sel_color
		surf.fill(color, rect)
