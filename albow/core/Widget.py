
import sys
import logging

from pygame import Rect
from pygame import Surface

from pygame.event import Event

from pygame.locals import K_RETURN
from pygame.locals import K_KP_ENTER
from pygame.locals import K_ESCAPE
from pygame.locals import K_TAB
from pygame.locals import KEYDOWN
from pygame.locals import SRCALPHA

from pygame.mouse import set_cursor
from pygame.cursors import arrow as arrow_cursor
from pygame.transform import rotozoom
from albow.vectors import add
from albow.vectors import subtract
from albow.utils import frame_rect

from albow.utils import overridable_property

from albow.themes.ThemeProperty import ThemeProperty
from albow.themes.FontProperty import FontProperty

from albow.themes.Theme import themeRoot

debug_rect = False
debug_tab = True

root_widget = None
current_cursor = None


def rect_property(name):

    def get(self):
        return getattr(self._rect, name)

    def set(self, value):

        r = self._rect
        old_size = r.size
        setattr(r, name, value)
        new_size = r.size
        #
        # Python 3 update
        # i f old_size <> new_size:
        if old_size != new_size:
            #
            # Method signature changed since tuples not allowed to be passed
            #
            # self._resized(old_size)
            self._resized(old_size[0], old_size[1])

    return property(get, set)


class Widget:
    """
    The Widget class is the base class for all widgets. A widget occupies a rectangular area of the PyGame screen
    to which all drawing in it is clipped, and it may receive mouse and keyboard events. A widget may also
    contain subwidgets.

    .. Note::
        Due to a limitation of PyGame subsurfaces, a widget's rectangle must be entirely contained within that of
        its parent widget. An exception will occur if this is violated.


    - Reading the following attributes retrieves the corresponding values from the widget's rect.
    - Assigning to them changes the size and position of the widget.
    - Additionally, if the size of the widget is changed via these
      attributes, the size and position of its subwidgets is updated according to each subwidget's anchor attribute.

        <pre>
        left, right, top, bottom, width, height, size,
        topleft, topright, bottomleft, bottomright,
        midleft, midright, midtop, midbottom,
        center, centerx, centery
        </pre>

    This does not happen if the rect is modified directly.

    """

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
    """
    Font to use for drawing text in the widget. How this property is used depends on the widget. Some widgets have 
    additional font properties for specific parts of the widget.
    """
    fg_color = ThemeProperty('fg_color')
    """
    Foreground colour for the contents of the widget. How this property is used depends on the widget. Some widgets 
    have additional colour properties for specific parts of the widget.
    """
    bg_color = ThemeProperty('bg_color')
    """
    Background colour of the widget. If specified, the widget's rect is filled with this colour before drawing its 
    contents. If no background colour is specified or it is set to None, the widget has no background and is drawn 
    transparently over its parent. For most widgets, it defaults to None.
    """
    bg_image = ThemeProperty('bg_image')
    """
    An image to be displayed in the background. If specified, this overrides any bg_color.
    """
    scale_bg = ThemeProperty('scale_bg')
    """
    If true, and the background image is smaller than the widget in either direction, the background image is scaled 
    to fill the widget, otherwise it is centered. Note: Due to a limitation of the pygame rotozoom function, scaling 
    is currently uniform in both directions, with the scale factor being that required to ensure that the whole 
    widget is covered.
    """
    border_width = ThemeProperty('border_width')
    """
    Width of a border to be drawn inside the outer edge of the widget. If this is unspecified or set to zero, 
    no border is drawn.
    """
    border_color = ThemeProperty('border_color')
    """
    Color in which to draw the border specified by border_width.
    """
    sel_color = ThemeProperty('sel_color')
    margin = ThemeProperty('margin')
    """
    The amount of space to leave between the edge of the widget and its contents. Note that this distance includes the 
    border_width, e.g. if border_width == 1 and margin == 3, then there is 2 pixels of space between the inside of 
    the border and the contents.

    Most of the predefined Albow widgets honour the margin property, but this is not automatic for your own widget 
    subclasses. You may find the get_margin_rect() method helpful in implementing support for the margin property 
    in your widget classes.
    """

    menu_bar = overridable_property('menu_bar')
    """
    A MenuBar to be attached to and managed by this widget. Assigning to the menu_bar property automatically adds the 
    menu bar as a child widget. Also, if the width of the menu bar has not already been set, it is set to be the same 
    width as this widget and to stretch horizontally with it.

    When a key down event with the platform's standard menu command modifier (Command on Mac, Control on other 
    platforms) is dispatched through this widget, the menu bar is first given a chance to handle the event. If the 
    menu bar does not handle it, dispatching continues as normal.

    """
    is_gl_container: bool = overridable_property('is_gl_container')
    """
    Controls the drawing behaviour of the widget when used in an OpenGL window. When true, 
    
    - no 2D drawing is performed for the widget itself
    - its background colour and border properties are ignored 
    - its draw() and draw_over() methods are never called. 
        
    If it has 3D subwidgets, 3D drawing is performed for them.

    When false, the widget and its subwidgets are rendered to a temporary surface which is then drawn to the window 
    using glDrawPixels() with blending. No 3D drawing is performed for any of its subwidgets.

    In either case, input events are handled in the usual way.

    This property has no effect on widgets in a non-OpenGL window.
    """

    tab_stop: bool = False
    """
    True if this widget should receive the keyboard focus when the user presses the Tab key. Defaults to false.
    """
    enter_response = None
    cancel_response = None
    anchor = 'lt'
    """
    A string specifying how this widget is to change in size and position when its parent widget changes size. The 
    letters 'l', 'r', 't' and 'b' are used to anchor the widget to the left, right, top or bottom sides of its 
    parent. Anchoring it to both left and right, or both top and bottom, causes the widget to stretch or shrink when 
    its parent changes in width or height.
    """
    _menubar = None
    _visible = True
    _is_gl_container = False
    redraw_every_event = True
    resizing_axes = {'h': 'lr', 'v': 'tb'}
    resizing_values = {'': [0], 'm': [1], 's': [0, 1]}

    visible = overridable_property('visible')
    """
    When true, the widget is visible and active. When false, the widget is invisible and will not receive events. 
    Defaults to true. The behaviour of this property can be customized by overriding the get_visible method.
    """
    parent = None
    """
    Read-only. The widget having this widget as a subwidget, or None if the widget is not contained in another 
    widget. A widget must ultimately be contained in the root widget in order to be drawn and to receive events.
    """
    subwidgets = []
    """
    """
    focus_switch: "Widget" = None
    """
    subwidget to receive key events
    """
    debug_resize = False


    def __init__(self, rect: Rect = None, **kwds):
        """
        Creates a new widget, initially without any parent. If a rect is given, it specifies the new widget's initial s
        ize and position relative to its parent.

        Args:
            rect:   A PyGame rectangle defining the portion of the parent widget's coordinate system occupied by the\
             widget. Modifying this rectangle changes the widget's size and position.

            **kwds: Additional attributes specified as key-value pairs
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
        #
        # Python 3 update no more tuples
        # self._resized(old_size)
        self._resized(old_size[0], old_size[1])

    rect = property(get_rect, set_rect)
    """
    bounds in parent's coordinates
    """

    def add_anchor(self, mode: str):
        """
        Adds the options specified by mode to the anchor property.

        Args:
            mode:  The new anchor mode to add

        Returns:

        """
        """
        """
        self.anchor = "".join(set(self.anchor) | set(mode))

    def remove_anchor(self, mode: str):
        """
         Remove the options specified by mode from anchor property.

        Args:
            mode: The anchor mode to remove
        Returns:

        """
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
    # update for 3.7
    # https://stackoverflow.com/questions/33837918/type-hints-solve-circular-dependency
    #
    def add(self, arg: 'Widget'):     # Python 3 forward reference;
        """
        Adds the given widget or sequence of widgets as a subwidget of this widget.

        Args:
            arg:  May be a single widget or multiple

        """
        if arg:

            self.logger.debug("arg: '%s' is Widget %s", arg.__str__(), isinstance(arg, Widget))
            #
            # Python 3 hack because 'Label' is sometimes reported as not a 'Widget'
            #
            if isinstance(arg, Widget) or not hasattr(arg, '__iter__' ):
                arg.set_parent(self)
            else:
                self.logger.debug("arg is container: %s", arg.__str__)
                for item in arg:
                    self.add(item)

    def add_centered(self, widget):
        """
        Adds the given widget and positions it in the center of this widget.

        Args:
            widget: The widget to center

        """
        w, h = self.size
        widget.center = w // 2, h // 2
        self.add(widget)

    def remove(self, widget):
        """

        If the given widget is a subwidget of this widget, it is removed and its parent attribute is set to None.

        Args:
            widget:  The widget to act on


        """
        if widget in self.subwidgets:
            widget.set_parent(None)

    def set_parent(self, parent):
        """
        Changes the parent of this widget to the given widget. This is an alternative to using the add and remove
        methods of the parent widget. Setting the parent to None removes the widget from any parent.

        Args:
            parent:

        """
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
        # print "Widget.draw_all:", self, "on", surface ###
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

        Args:
            event:   The event to augment

        """
        posMap = self.global_to_local(event.pos)
        # event.dict['local'] = self.global_to_local(event.pos)
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
        """
        If this widget or one of its subwidgets has the keyboard focus, returns that widget. Otherwise it returns
        the widget that would have the keyboard focus if this widget were on the focus path.

        Returns:  A widget with the focus

        """
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
        """
        If the widget has a method with the given name, it is called with the given arguments, and its return value is
        is returned. Otherwise, nothing is done and 'pass' is returned.

        Args:
            name:  The method name
            *args: The arguments to use

        Returns:  The value of the 'called' method

        """
        method = getattr(self, name, None)
        if method:
            return method(*args)
        else:
            return 'pass'

    def call_parent_handler(self, name, *args):
        """
        Invokes call_handler on the parent of this widget, if any. This can be used to pass an event on to a
        parent widget if you don't want to handle it.

        Args:
            name:   The method name
            *args:  Its arguments

        Returns:  The value of the 'called' methood

        """
        parent = self.next_handler()
        if parent:
            parent.call_handler(name, *args)

    def global_to_local(self, p):
        """
        Converts the given coordinate pair from PyGame screen coordinates to the widget's local coordinate system.

        Args:
            p:  The global coordinates

        Returns:  The widget's local coordinates

        """
        return subtract(p, self.local_to_global_offset())

    def local_to_global(self, p):
        """
        Converts the given coordinate pair from the widget's local coordinate system to PyGame screen coordinates.

        Args:
            p: Widget local coordinates

        Returns:

        """
        return add(p, self.local_to_global_offset())

    def local_to_global_offset(self):
        d = self.topleft
        parent = self.parent
        if parent:
            d = add(d, parent.local_to_global_offset())
        return d

    def get_global_rect(self):

        p = self.local_to_global_offset()
        #
        # Python 3 update
        #
        pTuple = tuple(p)
        s = self.rect.size
        #
        # Python 3 update
        #
        # return Rect(p, s)
        return Rect(pTuple, s)

    def is_inside(self, container):
        widget = self
        while widget:
            if widget is container:
                return True
            widget = widget.parent
        return False

    def present(self, centered: bool = True):

        """
        Presents the widget as a modal dialog. The widget is added as a subwidget of the root widget, centered
        within it if centered is true. A nested event loop is entered in which any events for widgets other
        than this widget and its subwidgets are ignored. Control is retained until this widget's dismiss
        method is called. The argument to dismiss is returned from the present call.

        Args:
            centered:  Indicates whether or not to center;  default is True

        Returns:  The value returned from the modal widget

        """
        #
        # TODO  Something about my re-packaging caused me to lose
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

        self.logger.debug("Widget.present: returning.  Result: %s", self.modal_result)
        return self.modal_result

    def dismiss(self, value=True):
        """
        When the presented widget presented is modal using present() causes the modal event loop to exit and
        the present() call to return with the given result.

        Args:
            value:  The value to set in modal_result

        Returns:

        """
        self.modal_result = value

    def get_root(self):
        """
        Returns the root widget (whether this widget is contained within it or not).

            Deprecated, use root.get_root()

        Returns:  The root widget

        """
        return root_widget

    def get_top_widget(self) -> "Widget":
        """
        Returns the highest widget in the containment hierarchy currently receiving input events. If a modal
        dialog is in progress, the modal dialog widget is the top widget, otherwise it is the root widget.

        Returns:  The top level widget in a containment hierarchy

        """
        top = self
        while top.parent and not top.is_modal:
            top = top.parent
        return top

    def focus(self):
        """
        Gives this widget the keyboard focus. The widget must be visible (i.e. contained within the root
        widget) for this to have any affect.

        """
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
        """

        Returns:    True if the widget is on the focus path, i.e. this widget or one of its subwidgets currently\
        has the keyboard focus.

        """
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
        """
        Marks the widget as needing to be redrawn. You will need to call this from the begin_frame() method of your
        Shell or Screen if you have the redraw_every_frame attribute of the root widget set to False.

        NOTE: Currently, calling this method on any widget will cause all widgets to be redrawn on the next return\
        to the event loop. Future versions may be more selective.

        """
        root = self.get_root()
        if root:
            root.do_draw = True

    def predict(self, kwds, name):
        try:
            return kwds[name]
        except KeyError:
            return themeRoot.get(self.__class__, name)

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
        return kwds.get(name) or themeRoot.get_font(self.__class__, name)

    def get_margin_rect(self) -> Rect:
        """
        Returns a Rect in local coordinates representing the content area of the widget, as determined
        by its margin property.

        Returns: The rect of the content area

        """
        r = Rect((0, 0), self.size)
        d = -2 * self.margin
        r.inflate_ip(d, d)
        return r

    def set_size_for_text(self, width, nLines=1):
        """
        Sets the widget's Rect to a suitable size for displaying text of the specified width and number of lines in
        its current font, as determined by the font property. The width can be either a number of pixels or a
        piece of sample text.

        Args:
            width:  The number of pixes or some sample text

            nLines: The number of lines in the text;  Defaults to 1


        """
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
            self.size = (width, height * nLines + d)

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

    def inherited(self, attributeName: str):
        """
        Looks up the parent hierarchy to find the first widget that has an attribute with the given name, and
        returns its value. If not found, returns None.

        Args:
            attributeName:  The name of the attribute

        Returns: The attribute's value or None if not found

        """
        value = getattr(self, attributeName)

        if value is not None:
            return value
        else:
            parent = self.next_handler()
            if parent:
                return parent.inherited(attributeName)

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

    def gl_draw_all(self, gl_surface):

        # print "Widget.gl_draw_all:", self, "on", gl_surface ###
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

        # print "Widget.gl_draw_self:", self ###
        gl_surface.gl_enter()
        # TODO: draw background and border here
        self.draw(gl_surface)
        gl_surface.gl_exit()

    def defer_drawing(self):
        """
        Called every time around the event loop on the root widget or a
        widget that is modal. If it returns true, the frame timer runs,
        scheduled calls are made, and screen updates are performed once per
        frame. Otherwise the screen is updated after each mouse down, mouser
        up or keyboard event and scheduled calls are not made.
        """
        return False

    def relative_mode(self):
        """
        Return true if relative input mode should be used. Called each
        time around the event loop on the root widget or a widget that is
        modal.

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

    def __contains__(self, event):
        r = Rect(self._rect)
        r.left = 0
        r.top = 0

        answer: bool = False
        try:
            p      = self.global_to_local(event.pos)
            pList  = list(p)
            answer = r.collidepoint(pList[0], pList[1])
        except AttributeError as ae:
            self.logger.error("Attribute error %s", ae.__repr__())
        #
        # Python 3 method signature change
        #
        # return r.collidepoint(p)
        # return r.collidepoint(pList[0], pList[1])
        return answer

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

    #
    #
    #   Abstract methods follow
    #
    #
    def draw(self, surface: Surface):
        """
        Called whenever the widget's contents need to be drawn. The surface is a subsurface the same size as the
        widget's rect with the drawing origin at its top left corner.

        The widget is filled with its background colour, if any, before this method is called. The border and
        subwidgets, if any, are drawn after this method returns.

        Args:
            surface:  The pygame surface to draw on
        """
        pass

    def draw_over(self, surface: Surface):
        """
        Called after drawing all the subwidgets of this widget. This method can be used to draw content that is
        to appear on top of any subwidgets.

        Args:
            surface:  The pygame surface to draw on
        """
        pass

    def key_down(self, theKeyEvent: Event):
        """
        Called when a key press event occurs and this widget has the keyboard focus, or a subwidget has the
        focus but did not handle the event.

        NOTE: If you override this method and don't want to handle a key_down event, be sure to call the inherited\
        key_down() method to pass the event to the parent widget.

        Args:
            theKeyEvent: The key event
        """
        k = theKeyEvent.key
        self.logger.debug("Widget.key_down: %s", k)

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
        self.call_parent_handler('key_down', theKeyEvent)

    def key_up(self, theKeyEvent: Event):
        """
        Called when a key release event occurs and this widget has the keyboard focus.

        NOTE:
            - If you override this method and don't want to handle a key_up event
            - be sure to call the inherited key_up() method to pass the event to the parent widget.

        Args:
            theKeyEvent:  The key event

        """
        self.call_parent_handler('key_up', theKeyEvent)

    def get_cursor(self, event):
        """
        Called to determine the appropriate cursor to display over the widget.
        The ResourceUtility.get_cursor() function returns a suitable tuple.

        Args:
            event:  An event object containing the mouse coordinates to be used in determining the cursor.

        Returns: A cursor in the form of a tuple of arguments to the PyGame set_cursor() function


        """
        return arrow_cursor

    def attention_lost(self):
        """
        Called when the widget is on the focus path, and a mouse-down event occurs in any widget which is not on
        the focus path. The focus path is defined as the widget having the keyboard focus, plus any widgets on the
        path from there up the parent hierarchy to the root widget. This method can be useful to ensure that changes
        to a data structure being edited are committed before performing some other action.

        """
        pass

    def resized(self, dw, dh):
        """
        Called when the widget changes size as a result of assigning to its width, height or size attributes,
        with (dw, dh) being the amount of the change. The default is to call parent_resized on each of its subwidgets.

        Args:
            dw:  width
            dh:  height

        Returns:

        """
        if self.debug_resize:
            self.logger.info("Widget.resized: %s by: (%s, %s) to %s", self, dw, dh, self.size)
        for widget in self.subwidgets:
            widget.parent_resized(dw, dh)

    def parent_resized(self, dw, dh):
        """
        Called when the widget's parent changes size as a result of assigning to its width, height or size
        attributes, with (dw, dh) being the amount of the change. The default is to resize and/or reposition
        the widget according to its anchor attribute.

        Args:
            dw:  Width
            dh:  Height

        """
        debug_resize = self.debug_resize or self.parent.debug_resize

        if debug_resize:
            self.logger.info("Widget_parent_resized %s, by (%s, %s)", self, dw, dh)

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
                self.logger.info("Widget.parent_resized: changing rect to (%s, %s, %s, %s)", left, top, width, height)
            self.rect = (left, top, width, height)
        elif move:
            if debug_resize:
                self.logger.info("Widget.parent_resized: moving to (%s,%s)", left, top)
            self._rect.topleft = (left, top)

    def get_visible(self):
        """
        Called to determine the value of the visible property. By overriding this, you can make the visibility of the
        widget dependent on some external condition.

        Returns: The widget visibility state

        """
        return self._visible

    def set_visible(self, x):
        self._visible = x
