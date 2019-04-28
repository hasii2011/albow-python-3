#---------------------------------------------------------------------------
#
#   Albow - Root widget
#
#---------------------------------------------------------------------------

import sys
from time import time, sleep
import pygame
from pygame.locals import *
from pygame.time import Clock, get_ticks, set_timer as set_pygame_timer
from pygame.event import Event, get_grab, set_grab
from pygame.mouse import set_visible as set_mouse_visible
import Widget
from Widget import Widget

mod_cmd = KMOD_LCTRL | KMOD_RCTRL | KMOD_LMETA | KMOD_RMETA
double_click_time = 300 # milliseconds

modifiers = dict(
    shift = False,
    ctrl = False,
    alt = False,
    meta = False,
)

modkeys = {
    K_LSHIFT: 'shift',  K_RSHIFT: 'shift',
    K_LCTRL:  'ctrl',   K_RCTRL:  'ctrl',
    K_LALT:   'alt',    K_RALT:   'alt',
    K_LMETA:  'meta',   K_RMETA:  'meta',
}

MUSIC_END_EVENT = USEREVENT + 1

last_mouse_event = Event(0, pos = (0, 0), local = (0, 0))
last_mouse_event_handler = None
root_widget = None     # Root of the containment hierarchy
top_widget = None      # Initial dispatch target
clicked_widget = None  # Target of mouse_drag and mouse_up events
timer_event = None     # Timer event pending delivery
next_frame_due = 0.0   #


class ApplicationError(Exception):
    pass


class Cancel(ApplicationError):
    pass


def set_modifier(key, value):
    attr = modkeys.get(key)
    if attr:
        modifiers[attr] = value


def add_modifiers(event):
    d = event.dict
    d.update(modifiers)
    d['cmd'] = event.ctrl or event.meta


def get_root():
    return root_widget


def get_top_widget():
    return top_widget


def get_focus():
    return top_widget.get_focus()


def init_timebase():
    global time_base
    time_base = time() * 1000.0 - get_ticks()


def timestamp():
    return time() * 1000.0 - time_base

#---------------------------------------------------------------------------

class RootWidget(Widget):
    #
    #  surface   Pygame display surface
    #  is_gl     True if OpenGL surface

    redraw_every_frame = False
    do_draw            = False
    _is_gl_container   = True
    frame_time         = 0.0
    _use_sleep         = True

    def __init__(self, surface, **kwds):
        """

        :param surface:
        :param kwds:
        """
        global root_widget
        #
        # Python 3 update
        #
        # Widget.__init__(self, surface.get_rect())
        super().__init__(surface.get_rect(), **kwds)

        init_timebase()
        self.surface = surface
        root_widget = self
        Widget.root_widget = self
        #
        # Python 3 update
        #
        # self.is_gl = surface.get_flags() & OPENGL <> 0
        self.is_gl = surface.get_flags() & OPENGL != 0
        if self.is_gl:

            from opengl import GLSurface
            self.gl_surface = GLSurface(surface, self.rect)

    def set_timer(self, ms):
        self.frame_time = ms
        if not self._use_sleep:
            set_pygame_timer(USEREVENT, max(1, int(round(ms))))

    def run(self):
        self.run_modal(None)

    def run_modal(self, modal_widget):
        global last_mouse_event, last_mouse_event_handler
        global top_widget, clicked_widget
        global timer_event
        global next_frame_due
        is_modal = modal_widget is not None
        modal_widget = modal_widget or self
        relative_pause = False
        relative_warmup = 0
        try:
            old_top_widget = top_widget
            top_widget = modal_widget
            was_modal = modal_widget.is_modal
            modal_widget.is_modal = True
            modal_widget.modal_result = None
            if not modal_widget.focus_switch:
                modal_widget.tab_to_first()
            mouse_widget = None
            # if clicked_widget:
            #	clicked_widget = modal_widget
            num_clicks = 0
            last_click_time = 0
            self.do_draw = True
            use_sleep = self._use_sleep
            while modal_widget.modal_result is None:
                # print "RootWidget: frame_time =", self.frame_time ###
                #
                # Python 3 update
                #
                # defer_drawing = self.frame_time <> 0.0 and modal_widget.defer_drawing()
                defer_drawing = self.frame_time != 0.0 and modal_widget.defer_drawing()
                try:
                    if not is_modal:
                        if timer_event:
                            if not use_sleep and defer_drawing:
                                make_scheduled_calls()
                            add_modifiers(timer_event)
                            if last_mouse_event:
                                timer_event.dict['pos'] = last_mouse_event.pos
                                timer_event.dict['local'] = last_mouse_event.local
                            if last_mouse_event_handler:
                                last_mouse_event_handler.setup_cursor(timer_event)
                            self.do_draw = self.timer_event(timer_event)
                            timer_event = None
                        else:
                            if defer_drawing:
                                # print "RootWidget: Clearing do_draw because of defer_drawing" ###
                                self.do_draw = False
                    # print "RootWidget: do_draw =", self.do_draw ###
                    if self.do_draw:
                        if self.is_gl:
                            # self.gl_clear()
                            # self.gl_draw_all(self, (0, 0))
                            # GL.glFlush()
                            gl_surface = self.gl_surface
                            gl_surface.gl_clear(self.bg_color)
                            self.gl_draw_all(gl_surface)
                            gl_surface.gl_flush()
                        else:
                            self.draw_all(self.surface)
                        self.do_draw = False
                        # tb1 = timestamp() ###
                        pygame.display.flip()
                    # tb2 = timestamp() ###
                    # print "RootWidget: Flip block  %5d" % (tb2 - tb1) ###
                    in_relative_mode = bool(modal_widget.relative_mode())
                    grab = in_relative_mode and not relative_pause
                    # if grab <> get_grab():
                    if grab != get_grab():
                        set_grab(grab)
                        set_mouse_visible(not grab)
                        relative_warmup = 3 # Ignore spurious deltas on entering relative mode
                    # tb1 = timestamp() ###
                    # print "RootWidget: use_sleep =", use_sleep, "defer_drawing =", defer_drawing ###
                    if use_sleep and defer_drawing:
                        # print "RootWidget: Handling timing" ###
                        time_now = timestamp()
                        # print "RootWidget: Time is now", time_now ###
                        if next_frame_due < time_now:
                            #print "RootWidget: Adjusting next frame due time to time now" ###
                            next_frame_due = time_now
                        # print "RootWidget: Waiting for next frame due at", next_frame_due ###
                        while 1:
                            sleep_time = make_due_calls(time_now, next_frame_due)
                            if sleep_time <= 0.0:
                                break
                            #print "RootWidget: Sleeping for", sleep_time ###
                            sleep(sleep_time / 1000.0)
                            time_now = timestamp()
                        next_frame_due += self.frame_time
                        # print "RootWidget: Next frame now due at", next_frame_due ###
                        timer_event = Event(USEREVENT, time = time_now)
                        events = []
                    else:
                        events = [pygame.event.wait()]
                    # tb2 = timestamp() ###
                    # tb = tb2 - tb1 ###
                    # if tb: ###
                    #	print "RootWidget: Event block %5d" % tb ###
                    events.extend(pygame.event.get())
                    for event in events:
                        t = timestamp()
                        event.dict['time'] = t
                        event.dict['local'] = getattr(event, 'pos', (0, 0))
                        type = event.type
                        if type == QUIT:
                            self.quit()
                        elif type == MOUSEBUTTONDOWN:
                            #print "RootWidget: MOUSEBUTTONDOWN: setting do_draw" ###
                            self.do_draw = True
                            if t - last_click_time <= double_click_time:
                                num_clicks += 1
                            else:
                                num_clicks = 1
                            last_click_time = t
                            event.dict['num_clicks'] = num_clicks
                            add_modifiers(event)
                            last_mouse_event = event
                            if in_relative_mode:
                                event.dict['local'] = (0, 0)
                                if relative_pause:
                                    relative_pause = False
                                else:
                                    #modal_widget.dispatch_key('mouse_down', event)
                                    mouse_widget = modal_widget.get_focus()
                                    clicked_widget = mouse_widget
                                    last_mouse_event_handler = mouse_widget
                                    mouse_widget.handle_event('mouse_down', event)
                            else:
                                mouse_widget = self.find_widget(event.pos)
                                if not mouse_widget.is_inside(modal_widget):
                                    mouse_widget = modal_widget
                                clicked_widget = mouse_widget
                                last_mouse_event_handler = mouse_widget
                                mouse_widget.notify_attention_loss()
                                mouse_widget.handle_mouse('mouse_down', event)
                        elif type == MOUSEMOTION:
                            add_modifiers(event)
                            last_mouse_event = event
                            if in_relative_mode:
                                event.dict['local'] = (0, 0)
                                if not relative_pause:
                                    if relative_warmup:
                                        relative_warmup -= 1
                                    else:
                                        #modal_widget.dispatch_key('mouse_delta', event)
                                        mouse_widget = clicked_widget or modal_widget.get_focus()
                                        last_mouse_event_handler = mouse_widget
                                        mouse_widget.handle_event('mouse_delta', event)
                            else:
                                mouse_widget = self.find_widget(event.pos) # Do this in else branch?
                                if clicked_widget:
                                    last_mouse_event_handler = mouse_widget # Should this be clicked_widget?
                                    clicked_widget.handle_mouse('mouse_drag', event)
                                else:
                                    if not mouse_widget.is_inside(modal_widget):
                                        mouse_widget = modal_widget
                                    last_mouse_event_handler = mouse_widget
                                    mouse_widget.handle_mouse('mouse_move', event)
                        elif type == MOUSEBUTTONUP:
                            add_modifiers(event)
                            last_mouse_event = event
                            self.do_draw = True
                            if in_relative_mode:
                                event.dict['local'] = (0, 0)
                                if not relative_pause:

                                    if clicked_widget:
                                        mouse_widget = clicked_widget
                                        clicked_widget = None
                                    else:
                                        mouse_widget = modal_widget.get_focus()
                                    last_mouse_event_handler = mouse_widget
                                    mouse_widget.handle_event('mouse_up', event)
                            else:
                                mouse_widget = self.find_widget(event.pos) # Not necessary?
                                if clicked_widget:
                                    last_mouse_event_handler = clicked_widget
                                    clicked_widget = None
                                    last_mouse_event_handler.handle_mouse('mouse_up', event)
                        elif type == KEYDOWN:
                            key = event.key
                            if key == K_ESCAPE and in_relative_mode and \
                                    event.mod & KMOD_CTRL and event.mod & KMOD_SHIFT:
                                relative_pause = True
                            elif relative_pause:
                                relative_pause = False
                            else:
                                set_modifier(key, True)
                                self.do_draw = True
                                self.send_key(modal_widget, 'key_down', event)
                                if last_mouse_event_handler:
                                    event.dict['pos'] = last_mouse_event.pos
                                    event.dict['local'] = last_mouse_event.local
                                    last_mouse_event_handler.setup_cursor(event)
                        elif type == KEYUP:
                            key = event.key
                            set_modifier(key, False)
                            self.do_draw = True
                            self.send_key(modal_widget, 'key_up', event)
                            if last_mouse_event_handler:
                                event.dict['pos'] = last_mouse_event.pos
                                event.dict['local'] = last_mouse_event.local
                                last_mouse_event_handler.setup_cursor(event)
                        elif type == MUSIC_END_EVENT:
                            self.music_end()
                        elif type == USEREVENT:
                            if defer_drawing and not use_sleep:
                                timer_event = event
                except Cancel:
                    pass
                #
                # Python 3 update
                #
                # except ApplicationError, e:
                except ApplicationError as e:
                    self.report_error(e)
        finally:
            modal_widget.is_modal = was_modal
            top_widget = old_top_widget
        clicked_widget = None

    def send_key(self, widget, name, event):
        add_modifiers(event)
        widget.dispatch_key(name, event)

    def defer_drawing(self):
        return True

    def timer_event(self, event):
        self.begin_frame()
        return True

    def begin_frame(self):
        """Deprecated, use timer_event() instead."""
        pass

    def get_root(self):
        return self

    def has_focus(self):
        return True

    def quit(self):
        if self.confirm_quit():
            sys.exit(0)

    def confirm_quit(self):
        return True

    def get_mouse_for(self, widget):
        last = last_mouse_event
        event = Event(0, last.dict)
        event.dict['local'] = widget.global_to_local(event.pos)
        add_modifiers(event)
        return event

    #	def gl_clear(self):
    #		bg = self.bg_color
    #		if bg:
    #			r = bg[0] / 255.0
    #			g = bg[1] / 255.0
    #			b = bg[2] / 255.0
    #			GL.glClearColor(r, g, b, 0.0)
    #		GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT
    #			| GL.GL_ACCUM_BUFFER_BIT | GL.GL_STENCIL_BUFFER_BIT)

    def music_end(self):
        import music
        music.music_end()

    #	def pause_relative_mode(self):
    #		set_grab(False)
    #		set_mouse_visible(True)
    #		while 1:
    #			e = event.wait()
    #			type = e.type
    #			if type == MOUSEBUTTONDOWN or type == KEYDOWN:
    #				return

    def report_error(self, e):
        pass


from time import time
from bisect import insort

scheduled_calls = []


def make_scheduled_calls():
    #  Legacy
    sched = scheduled_calls
    t = timestamp()
    while sched and sched[0][0] <= t:
        sched[0][1]()
        sched.pop(0)


class ScheduledCall:

    def __init__(self, time, func, interval):
        self.time = time
        self.func = func
        self.interval = interval

    def __cmp__(self, other):
        return cmp(self.time, other.time)


def make_due_calls(time_now, until_time):
    #  Call all functions scheduled at or before time_now.
    #  Return the time remaining until the next scheduled call
    #  or until_time, whichever is sooner.
    # print "albow.root.make_due_calls:", time_now, until_time ###
    sched = scheduled_calls
    while sched and sched[0].time <= time_now:
        item = sched.pop(0)
        item.func()
        delay = item.interval
        if delay:
            next_time = item.time + delay
            if next_time < time_now:
                next_time = time_now + delay
            #print "albow.root.make_due_calls: rescheduling at", next_time ###
            item.time = next_time
            insort(sched, item)
    if sched:
        next_time = min(until_time, sched[0].time)
    else:
        next_time = until_time
    return next_time - time_now


def schedule(delay, func):
    """
    Deprecated, use schedule_call or schedule_event instead.
    """
    schedule_call(delay * 1000.0, func)


def schedule_call(delay, func, repeat = False):
    """
    Arrange for the given function to be called after the specified
    delay in milliseconds. Scheduled functions are called synchronously from
    the event loop, and only when the frame timer is running. If repeat is
    true, call will be made repeatedly at the specified interval, otherwise
    it will only be made once.
    """
    t = timestamp() + delay
    if repeat:
        r = delay
    else:
        r = 0.0
    item = ScheduledCall(t, func, r)
    insort(scheduled_calls, item)
    return item


def schedule_event(delay, func, repeat = False):
    def thunk():
        event = Event(USEREVENT, time = timestamp())
        add_modifiers(event)
        func(event)
    schedule_call(delay, thunk, repeat)


def cancel_call(token):
    """
    Cancel a previously scheduled call, given a token returned by
    schedule_call or schedule_event.
    """
    try:
        scheduled_calls.remove(token)
    except ValueError:
        pass
