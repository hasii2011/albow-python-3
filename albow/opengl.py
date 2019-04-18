#-------------------------------------------------------------------------
#
#   Albow - OpenGL widgets
#
#-------------------------------------------------------------------------

from __future__ import division
from pygame import Rect, image
from pygame.display import get_surface as get_display
from OpenGL import GL, GLU
from widget import Widget

class GLViewport(Widget):

	is_gl_container = True

	def gl_draw_self(self, root, offset):
		rect = self.rect.move(offset)
	
	def gl_draw_self(self, gl_surface):
		# GL_CLIENT_ALL_ATTRIB_BITS is borked: defined as -1 but
		# glPushClientAttrib insists on an unsigned long.
		GL.glPushClientAttrib(0xffffffff)
		GL.glPushAttrib(GL.GL_ALL_ATTRIB_BITS)
		#GL.glViewport(rect.left, root.height - rect.bottom, rect.width, rect.height)
		self.gl_draw_viewport()
		GL.glPopAttrib()
		GL.glPopClientAttrib()
	
	def gl_draw_viewport(self):
		self.setup_matrices()
		self.gl_draw()
	
	def setup_matrices(self):
		rect = self.get_global_rect()
		win_height = get_display().get_height()
		GL.glViewport(rect.left, win_height - rect.bottom, rect.width, rect.height)
		GL.glMatrixMode(GL.GL_PROJECTION)
		GL.glLoadIdentity()
		self.setup_projection()
		GL.glMatrixMode(GL.GL_MODELVIEW)
		GL.glLoadIdentity()
		self.setup_modelview()

	def setup_projection(self):
		pass
	
	def setup_modelview(self):
		pass
	
	def gl_draw(self):
		pass
	
	def augment_mouse_event(self, event):
		Widget.augment_mouse_event(self, event)
		w, h = self.size
		viewport = (0, 0, w, h)
		self.setup_matrices()
		#gf = GL.glGetFloatv
		gf = GL.glGetDoublev
		pr_mat = gf(GL.GL_PROJECTION_MATRIX)
		mv_mat = gf(GL.GL_MODELVIEW_MATRIX)
		x, y = event.local
		y = h - y
		up = GLU.gluUnProject
		p0 = up(x, y, 0.0, mv_mat, pr_mat, viewport)
		p1 = up(x, y, 1.0, mv_mat, pr_mat, viewport)
		event.dict['ray'] = (p0, p1)
	
#-------------------------------------------------------------------------

class GLOrtho(GLViewport):

	def __init__(self, rect = None,
			xmin = -1, xmax = 1, ymin = -1, ymax = 1,
			near = -1, far = 1, **kwds):
		GLViewport.__init__(self, rect, **kwds)
		self.xmin = xmin
		self.xmax = xmax
		self.ymin = ymin
		self.ymax = ymax
		self.near = near
		self.far = far
	
	def setup_projection(self):
		GL.glOrtho(self.xmin, self.xmax, self.ymin, self.ymax,
			self.near, self.far)

#-------------------------------------------------------------------------

class GLPerspective(GLViewport):

	def __init__(self, rect = None, fovy = 20,
			near = 0.1, far = 1000, **kwds):
		GLViewport.__init__(self, rect, **kwds)
		self.fovy = fovy
		self.near = near
		self.far = far
	
	def setup_projection(self):
		aspect = self.width / self.height
		GLU.gluPerspective(self.fovy, aspect, self.near, self.far)

#-------------------------------------------------------------------------

class GLSurface(object):

	def __init__(self, display, rect):
		self.display = display
		self.rect = rect
	
	def gl_set_viewport(self):
		r = self.rect
		w = r.width
		h = r.height
	
	def gl_enter(self):
		r = self.rect
		w = r.width
		h = r.height
		gl = GL
		win_height = self.display.get_height()
		gl.glViewport(r.left, win_height - r.bottom, r.width, r.height)
		gl.glMatrixMode(gl.GL_PROJECTION)
		gl.glLoadIdentity()
		GLU.gluOrtho2D(0, w, h, 0)
		gl.glMatrixMode(gl.GL_MODELVIEW)
		gl.glLoadIdentity()
		gl.glPushAttrib(gl.GL_COLOR_BUFFER_BIT)
		gl.glDisable(gl.GL_DEPTH_TEST)
		gl.glEnable(gl.GL_BLEND)
		gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)

	def gl_exit(self):
		GL.glPopAttrib()
	
	def gl_clear(self, bg):
		if bg:
			r = bg[0] / 255.0
			g = bg[1] / 255.0
			b = bg[2] / 255.0
			GL.glClearColor(r, g, b, 0.0)
		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT
			| GL.GL_ACCUM_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT)
		
	def gl_flush(self):
		GL.glFlush()

	def get_size(self):
		return self.rect.size
	
	def get_width(self):
		return self.rect.width
	
	def get_height(self):
		return self.rect.height
	
	def get_rect(self):
		return Rect(self.rect)
	
	def blit(self, src, dst = (0, 0), area = None, flags = 0):
		# TODO: flags
		#print "GLSurface.blit:", src, "at", dst, "area =", area ###
		if isinstance(dst, Rect):
			dst = dst.topleft
		x, y = dst
		if area is not None:
			area = area.clip(src.get_rect())
			src = src.subsurface(area)
			x += area.left
			y += area.top
		w, h = src.get_size()
		data = image.tostring(src, 'RGBA', 1)
		#print "GLSurface: Drawing %sx%s pixels at %s,%s" % (w, h, x, y + h) ###
		gl = GL
		gl.glRasterPos2i(x, y + h)
		gl.glDrawPixels(w, h, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, data)
	
	def fill(self, color, rect = None, flags = 0):
		# TODO: flags
		if rect:
			x, y, w, h = rect
		else:
			x = y = 0
			w, h = self.rect.size
		gl = GL
		gl.glColor4ubv(color)
		gl.glBegin(GL.GL_QUADS)
		v = GL.glVertex2i
		v(x, y)
		v(x+w, y)
		v(x+w, y+h)
		v(x, y+h)
		gl.glEnd()

	def subsurface(self, rect):
		r = self.rect
		subrect = rect.move(r.left, r.top)
		return GLSurface(self.display, r.clip(subrect))

