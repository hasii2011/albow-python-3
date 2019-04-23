from __future__ import division
import sys
import logging

from pygame import Rect, Surface, draw, image
from pygame.locals import K_RETURN, K_KP_ENTER, K_ESCAPE, K_TAB, KEYDOWN, SRCALPHA
from pygame.mouse import set_cursor
from pygame.cursors import arrow as arrow_cursor
from pygame.transform import rotozoom
from vectors import add, subtract
from utils import frame_rect
import theme
from albow.theme import ThemeProperty, FontProperty


debug_rect = False
debug_tab = True

root_widget = None
current_cursor = None

def overridable_property(name, doc = None):
    """Creates a property which calls methods get_xxx and set_xxx of
    the underlying object to get and set the property value, so that
    the property's behaviour may be easily overridden by subclasses."""

    getter_name = sys.intern('get_' + name)
    setter_name = sys.intern('set_' + name)
    return property(
        lambda self: getattr(self, getter_name)(),
        lambda self, value: getattr(self, setter_name)(value),
        None,
        doc)

def rect_property(name):

    def get(self):
        return getattr(self._rect, name)
    def set(self, value):

        r = self._rect
        old_size = r.size
        setattr(r, name, value)
        new_size = r.size
        #if old_size <> new_size:       Python 3 update
        if old_size != new_size:
            #
            # Method signature changed since tuples not allowed to be passed
            #
            # self._resized(old_size)
            self._resized(old_size[0],old_size[1])

    return property(get, set)


class Widget(object):
    #  rect            Rect       bounds in parent's coordinates
    #  parent          Widget     containing widget
    #  subwidgets      [Widget]   contained widgets
    #  focus_switch    Widget     subwidget to receive key events
    #  fg_color        color      or None to inherit from parent
    #  bg_color        color      to fill background, or None
    #  visible         boolean
    #  border_width    int        width of border to draw around widget, or None
    #  border_color    color      or None to use widget foreground color
    #  tab_stop        boolean    stop on this widget when tabbing
    #  anchor          string     of 'ltrb'

    debug_resize = False

    left = rect_property('left')
    right = rect_property('right')
    top = rect_property('top')
    bottom = rect_property('bottom')
    width = rect_property('width')
    height = rect_property('height')
    size = rect_property('size')
    topleft = rect_property('topleft')
    topright = rect_property('topright')
    bottomleft = rect_property('bottomleft')
    bottomright = rect_property('bottomright')
    midleft = rect_property('midleft')
    midright = rect_property('midright')
    midtop = rect_property('midtop')
    midbottom = rect_property('midbottom')
    center = rect_property('center')
    centerx = rect_property('centerx')
    centery = rect_property('centery')

    font = FontProperty('font')
    fg_color = ThemeProperty('fg_color')
    bg_color = ThemeProperty('bg_color')
    bg_image = ThemeProperty('bg_image')
    scale_bg = ThemeProperty('scale_bg')
    border_width = ThemeProperty('border_width')
    border_color = ThemeProperty('border_color')
    sel_color = ThemeProperty('sel_color')
    margin = ThemeProperty('margin')
    menu_bar = overridable_property('menu_bar')
    is_gl_container = overridable_property('is_gl_container')

    tab_stop = False
    enter_response = None
    cancel_response = None
    anchor = 'lt'
    _menubar = None
    _visible = True
    _is_gl_container = False
    redraw_every_event = True
    resizing_axes = {'h': 'lr', 'v': 'tb'}
    resizing_values = {'': [0], 'm': [1], 's': [0, 1]}

    visible = overridable_property('visible')

    def __init__(self, rect: Rect=None, **kwds):
        """

        :param rect:
        :param kwds:
        """

        self.logger = logging.getLogger(__name__)

        if rect and not isinstance(rect, Rect):
            raise TypeError("Widget rect not a pygame.Rect")

        self._rect = Rect(rect or (0, 0, 100, 100))
        self.parent = None
        self.subwidgets = []
        self.focus_switch = None
        self.is_modal = False

        self.set(**kwds)

    def set(self, **kwds):
        #
        #
        #
        # for name, value in kwds.iteritems():  -- update for python 3 -- hasii
        for name, value in kwds.items():
            if not hasattr(self, name):
                raise TypeError("Unexpected keyword argument '%s'" % name)
            setattr(self, name, value)

    def get_rect(self):
        return self._rect

    def set_rect(self, x):
        old_size = self._rect.size
        self._rect = Rect(x)
        # self._resized(old_size)               #
        self._resized(old_size[0], old_size[1]) # Python 3 update no more tuples
                                                #

    rect = property(get_rect, set_rect)

    def add_anchor(self, mode):
        """Adds the options specified by mode to the anchor property."""
        self.anchor = "".join(set(self.anchor) | set(mode))
    def remove_anchor(self, mode):
        """Remove the options specified by mode from anchor property."""
        self.anchor = "".join(set(self.anchor) - set(mode))

    def set_resizing(self, axis, value):
        chars = self.resizing_axes[axis]
        anchor = self.anchor
        for c in chars:
            anchor = anchor.replace(c, '')
        for i in self.resizing_values[value]:
            anchor += chars[i]
        self.anchor = anchor + value
    #
    # Python 3 update
    # def _resized(self, (old_width, old_height)): # remove tuple parameters
    #
    def _resized(self, old_width, old_height):
        """

        :param old_width:
        :param old_height:
        :return:
        """
        new_width, new_height = self._rect.size
        dw = new_width - old_width
        dh = new_height - old_height
        if dw or dh:
            self.resized(dw, dh)

    def resized(self, dw, dh):
        """

        :param dw:
        :param dh:
        :return:
        """
        if self.debug_resize:
            # print("Widget.resized:", self, "by", (dw, dh), "to", self.size)
            self.logger.info("Widget.resized: %s by: (%s, %s) to %s", self, dw, dh, self.size)
        for widget in self.subwidgets:
            widget.parent_resized(dw, dh)

    def parent_resized(self, dw, dh):
        debug_resize = self.debug_resize or self.parent.debug_resize
        if debug_resize:
            # print("Widget.parent_resized:", self, "by", (dw, dh))
            self.logger.info("Widget_parent_resized %s, by (%s, %s)", self, dw,dh)
        left, top, width, height = self._rect
        move = False
        resize = False
        anchor = self.anchor
        if dw and 'r' in anchor:
            if 'l' in anchor:
                resize = True
                width += dw
            else:
                move = True
                left += dw
        if dh and 'b' in anchor:
            if 't' in anchor:
                resize = True
                height += dh
            else:
                move = True
                top += dh
        if resize:
            if debug_resize:
                print("Widget.parent_resized: changing rect to", (left, top, width, height))
            self.rect = (left, top, width, height)
        elif move:
            if debug_resize:
                print("Widget.parent_resized: moving to", (left, top))
            self._rect.topleft = (left, top)

    def get_visible(self):
        return self._visible

    def set_visible(self, x):
        self._visible = x

    #
    # update for 3.7
    # https://stackoverflow.com/questions/33837918/type-hints-solve-circular-dependency
    #
    def add(self, arg: 'Widget'):     # Python 3 forward reference;

        if arg:

            # print("arg: '{}' is Widget:  '{}'".format(arg.__str__(),isinstance(arg, Widget)))
            self.logger.debug("arg: '%s' is Widget %s", arg.__str__(), isinstance(arg, Widget))
            #
            # Python 3 hack because 'Label' is sometimes reported as not a 'Widget'
            #
            if isinstance(arg, Widget) or not hasattr(arg, '__iter__' ):
                arg.set_parent(self)
            else:
                #print("arg: {}".format(arg.__str__()))
                self.logger.debug("arg is container: %s", arg.__str__)
                for item in arg:
                    self.add(item)

    def add_centered(self, widget):
        w, h = self.size
        widget.center = w // 2, h // 2
        self.add(widget)

    def remove(self, widget):
        if widget in self.subwidgets:
            widget.set_parent(None)

    def set_parent(self, parent):
        if parent is not self.parent:
            if self.parent:
                self.parent._remove(self)
            self.parent = parent
            if parent:
                parent._add(self)

    def _add(self, widget):
        self.subwidgets.append(widget)

    def _remove(self, widget):
        self.subwidgets.remove(widget)
        if self.focus_switch is widget:
            self.focus_switch = None

    def draw_all(self, surface):
        #print "Widget.draw_all:", self, "on", surface ###
        if self.visible:
            surf_rect = surface.get_rect()
            bg_image = self.bg_image
            if bg_image:
                if self.scale_bg:
                    bg_width, bg_height = bg_image.get_size()
                    width, height = self.size
                    if width > bg_width or height > bg_height:
                        hscale = width / bg_width
                        vscale = height / bg_height
                        bg_image = rotozoom(bg_image, 0.0, max(hscale, vscale))
                r = bg_image.get_rect()
                r.center = surf_rect.center
                surface.blit(bg_image, r)
            else:
                bg = self.bg_color
                if bg:
                    surface.fill(bg)
            self.draw(surface)
            bw = self.border_width
            if bw:
                bc = self.border_color or self.fg_color
                frame_rect(surface, bc, surf_rect, bw)
            for widget in self.subwidgets:
                sub_rect = widget.rect
                if debug_rect:
                    print("Widget: Drawing subwidget %s of %s with rect %s" % (
                        widget, self, sub_rect))
                sub_rect = surf_rect.clip(sub_rect)
                if sub_rect.width > 0 and sub_rect.height > 0:
                    try:
                        sub = surface.subsurface(sub_rect)
                    #
                    # Python 3 update
                    #
                    # except ValueError, e:
                    except ValueError as e:
                        if str(e) == "subsurface rectangle outside surface area":
                            self.diagnose_subsurface_problem(surface, widget)
                        else:
                            raise
                    else:
                        widget.draw_all(sub)
            self.draw_over(surface)

    def diagnose_subsurface_problem(self, surface, widget):
        mess = "Widget %s %s outside parent surface %s %s" % (
            widget, widget.rect, self, surface.get_rect())
        sys.stderr.write("%s\n" % mess)
        surface.fill((255, 0, 0), widget.rect)

    def draw(self, surface):
        #print "Widget.draw:", self ###
        pass

    def draw_over(self, surface):
        pass

    def find_widget(self, pos: tuple):

        for widget in self.subwidgets[::-1]:
            if widget.visible:
                r = widget.rect
                #
                # Python 3 update
                #
                # if r.collidepoint(pos):
                if isinstance(pos, map):
                    pos = list(pos)
                if r.collidepoint(pos[0], pos[1]):
                    return widget.find_widget(subtract(pos, r.topleft))
        return self

    def handle_mouse(self, name, event):
        self.augment_mouse_event(event)
        self.call_handler(name, event)
        self.setup_cursor(event)

    def augment_mouse_event(self, event):
        """
        Python 3 update.  local really needs to be a list
        :param event:
        :return:
        """
        posMap = self.global_to_local(event.pos)
        #event.dict['local'] = self.global_to_local(event.pos)
        event.dict['local'] = list(posMap)

    def setup_cursor(self, event):
        global current_cursor
        cursor = self.get_cursor(event) or arrow_cursor
        if cursor is not current_cursor:
            set_cursor(*cursor)
            current_cursor = cursor

    def dispatch_key(self, name, event):
        if self.visible:
            if event.cmd and event.type == KEYDOWN:
                menubar = self._menubar
                if menubar and menubar.handle_command_key(event):
                    return
            widget = self.focus_switch
            if widget:
                widget.dispatch_key(name, event)
            else:
                self.call_handler(name, event)
        else:
            self.call_parent_handler(name, event)

    def handle_event(self, name, event):
        handler = getattr(self, name, None)
        if handler:
            return handler(event)
        else:
            parent = self.next_handler()
            if parent:
                return parent.handle_event(name, event)

    def get_focus(self):
        widget = self
        while 1:
            focus = widget.focus_switch
            if not focus:
                break
            widget = focus
        return widget

    def notify_attention_loss(self):
        widget = self
        while 1:
            if widget.is_modal:
                break
            parent = widget.parent
            if not parent:
                break
            focus = parent.focus_switch
            if focus and focus is not widget:
                focus.dispatch_attention_loss()
            widget = parent

    def dispatch_attention_loss(self):
        widget = self
        while widget:
            widget.attention_lost()
            widget = widget.focus_switch

    def attention_lost(self):
        pass

    def handle_command(self, name, *args):
        method = getattr(self, name, None)
        if method:
            return method(*args)
        else:
            parent = self.next_handler()
            if parent:
                return parent.handle_command(name, *args)

    def next_handler(self):
        if not self.is_modal:
            return self.parent

    def call_handler(self, name, *args):
        method = getattr(self, name, None)
        if method:
            return method(*args)
        else:
            return 'pass'

    def call_parent_handler(self, name, *args):
        parent = self.next_handler()
        if parent:
            parent.call_handler(name, *args)

    def global_to_local(self, p):
        return subtract(p, self.local_to_global_offset())

    def local_to_global(self, p):
        return add(p, self.local_to_global_offset())

    def local_to_global_offset(self):
        d = self.topleft
        parent = self.parent
        if parent:
            d = add(d, parent.local_to_global_offset())
        return d

    def get_global_rect(self):
        p = self.local_to_global_offset()
        s = self.rect.size
        return Rect(p, s)

    def key_down(self, event):
        k = event.key
        #print "Widget.key_down:", k ###
        if k == K_RETURN or k == K_KP_ENTER:
            if self.enter_response is not None:
                self.dismiss(self.enter_response)
                return
        elif k == K_ESCAPE:
            if self.cancel_response is not None:
                self.dismiss(self.cancel_response)
                return
        elif k == K_TAB:
            self.tab_to_next()
            return
        self.call_parent_handler('key_down', event)

    def key_up(self, event):
        self.call_parent_handler('key_up', event)

    def is_inside(self, container):
        widget = self
        while widget:
            if widget is container:
                return True
            widget = widget.parent
        return False

    def present(self, centered = True):

        #
        # TODO  somethjng about my re-packaging cause me to lose
        # visibility to the root widget;  Figure it out later
        #
        global root_widget
        # print "Widget: presenting with rect", self.rect
        # root = self.get_root()
        root = Widget.root_widget
        if centered:
            self.center = root.center
        root.add(self)
        root.run_modal(self)
        self.dispatch_attention_loss()
        root.remove(self)
        #print "Widget.present: returning", self.modal_result
        return self.modal_result

    def dismiss(self, value = True):
        self.modal_result = value

    def get_root(self):
        # Deprecated, use root.get_root()
        return root_widget

    def get_top_widget(self):
        top = self
        while top.parent and not top.is_modal:
            top = top.parent
        return top

    def focus(self):
        parent = self.next_handler()
        if parent:
            parent.focus_on(self)

    def focus_on(self, subwidget):
        old_focus = self.focus_switch
        if old_focus is not subwidget:
            if old_focus:
                old_focus.dispatch_attention_loss()
            self.focus_switch = subwidget
        self.focus()

    def has_focus(self):
        return self.is_modal or (self.parent and self.parent.focused_on(self))

    def focused_on(self, widget):
        return self.focus_switch is widget and self.has_focus()

    def focus_chain(self):
        result = []
        widget = self
        while widget:
            result.append(widget)
            widget = widget.focus_switch
        return result

    def shrink_wrap(self):
        contents = self.subwidgets
        if contents:
            rects = [widget.rect for widget in contents]
            # rmax = Rect.unionall(rects) # broken in PyGame 1.7.1
            rmax = rects.pop()
            for r in rects:
                rmax = rmax.union(r)
            #
            # Updated python 3 -- hasii
            #
            # self._rect.size = add(rmax.topleft, rmax.bottomright)
            self._rect.size = list(add(rmax.topleft, rmax.bottomright))

    def invalidate(self):
        root = self.get_root()
        if root:
            root.do_draw = True

    def get_cursor(self, event):
        return arrow_cursor

    def predict(self, kwds, name):
        try:
            return kwds[name]
        except KeyError:
            return theme.root.get(self.__class__, name)

    def predict_attr(self, kwds, name):
        try:
            return kwds[name]
        except KeyError:
            return getattr(self, name)

    def init_attr(self, kwds, name):
        try:
            return kwds.pop(name)
        except KeyError:
            return getattr(self, name)

    def predict_font(self, kwds, name='font'):
        return kwds.get(name) or theme.root.get_font(self.__class__, name)

    def get_margin_rect(self):
        r = Rect((0, 0), self.size)
        d = -2 * self.margin
        r.inflate_ip(d, d)
        return r

    def set_size_for_text(self, width, nlines = 1):
        if width is not None:
            font = self.font
            d = 2 * self.margin
            #
            # Python 3 update
            # if isinstance(width, basestring):
            if isinstance(width, str):
                width, height = font.size(width)
                width += d + 2
            else:
                height = font.size("X")[1]
            self.size = (width, height * nlines + d)

    def tab_to_first(self):
        chain = self.get_tab_order()
        if chain:
            chain[0].focus()

    def tab_to_next(self):
        top = self.get_top_widget()
        chain = top.get_tab_order()
        try:
            i = chain.index(self)
        except ValueError:
            return
        target = chain[(i + 1) % len(chain)]
        target.focus()

    def get_tab_order(self):
        result = []
        self.collect_tab_order(result)
        return result

    def collect_tab_order(self, result):
        if self.visible:
            if self.tab_stop:
                result.append(self)
            for child in self.subwidgets:
                child.collect_tab_order(result)

    def inherited(self, attribute):
        value = getattr(self, attribute)
        if value is not None:
            return value
        else:
            parent = self.next_handler()
            if parent:
                return parent.inherited(attribute)

    def __contains__(self, event):
        r = Rect(self._rect)
        r.left = 0
        r.top = 0
        p = self.global_to_local(event.pos)
        pList = list(p)
        #
        # Python 3 method signature change
        #
        # return r.collidepoint(p)
        return r.collidepoint(pList[0], pList[1])

    def get_mouse(self):
        root = self.get_root()
        return root.get_mouse_for(self)

    def get_menu_bar(self):
        return self._menubar

    def set_menu_bar(self, menubar):
        if menubar is not self._menubar:
            if self._menubar:
                self.remove(self._menubar)
            self._menubar = menubar
            if menubar:
                if menubar.width == 0:
                    menubar.width = self.width
                    menubar.anchor = 'lr'
                self.add(menubar)

    def get_is_gl_container(self):
        return self._is_gl_container

    def set_is_gl_container(self, x):
        self._is_gl_container = x

    #	def gl_draw_all(self, root, offset):
    #		from OpenGL import GL, GLU
    #		rect = self.rect.move(offset)
    #		if self.is_gl_container:
    #			self.gl_draw_self(root, offset)
    #			suboffset = rect.topleft
    #			for subwidget in self.subwidgets:
    #				subwidget.gl_draw_all(root, suboffset)
    #		else:
    #			surface = Surface(self.size, SRCALPHA)
    #			self.draw_all(surface)
    #			data = image.tostring(surface, 'RGBA', 1)
    #			w, h = root.size
    #			GL.glViewport(0, 0, w, h)
    #			GL.glMatrixMode(GL.GL_PROJECTION)
    #			GL.glLoadIdentity()
    #			GLU.gluOrtho2D(0, w, 0, h)
    #			GL.glMatrixMode(GL.GL_MODELVIEW)
    #			GL.glLoadIdentity()
    #			GL.glRasterPos2i(rect.left, h - rect.bottom)
    #			GL.glPushAttrib(GL.GL_COLOR_BUFFER_BIT)
    #			GL.glEnable(GL.GL_BLEND)
    #			GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    #			GL.glDrawPixels(self.width, self.height,
    #				GL.GL_RGBA, GL.GL_UNSIGNED_BYTE, data)
    #			GL.glPopAttrib()
    #
    #	def gl_draw_self(self, root, offset):
    #		pass

    def gl_draw_all(self, gl_surface):
        #print "Widget.gl_draw_all:", self, "on", gl_surface ###
        if self.visible:
            if self.is_gl_container:
                self.gl_draw_self(gl_surface)
                for subwidget in self.subwidgets:
                    gl_subsurface = gl_surface.subsurface(subwidget.rect)
                    subwidget.gl_draw_all(gl_subsurface)
            else:
                surface = Surface(self.size, SRCALPHA)
                self.draw_all(surface)
                gl_surface.gl_enter()
                gl_surface.blit(surface)
                gl_surface.gl_exit()

    def gl_draw_self(self, gl_surface):
        #print "Widget.gl_draw_self:", self ###
        gl_surface.gl_enter()
        # TODO: draw background and border here
        self.draw(gl_surface)
        gl_surface.gl_exit()

    def defer_drawing(self):
        """Called every time around the event loop on the root widget or a
        widget being run modally. If it returns true, the frame timer runs,
        scheduled calls are made, and screen updates are performed once per
        frame. Otherwise the screen is updated after each mouse down, mouser
        up or keyboard event and scheduled calls are not made."""
        return False

    def relative_mode(self):
        """Return true if relative input mode should be used. Called each
        time around the event loop on the root widget or a widget being run
        modally.

        In relative input mode, the mouse cursor is hidden and mouse
        movements are not constrained to the edges of the window. In this
        mode, mouse movement events are delivered to the widget having the
        keyboard focus by calling the 'mouse_delta' method. The 'rel'
        attribute of the event should be used to obtain the movement since
        the last mouse event. Mouse down and mouse up events are also
        delivered to the focus widget, using the usual methods.

        The user can always escape from relative mode temporarily by
        pressing Ctrl-Shift-Escape. Normal mouse functionality is restored
        and further input events are ignored until a mouse click or key
        press occurs.
        """
        return False
