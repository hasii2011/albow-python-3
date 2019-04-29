

import sys
from time import sleep

from pygame.locals import *

import pygame
from pygame.mouse import set_visible as set_mouse_visible
from pygame.time import set_timer as set_pygame_timer

from pygame import Surface

from pygame.event import Event
from pygame.event import get_grab
from pygame.event import set_grab

from albow.core.Widget import Widget

from albow.core.root import init_timebase

from albow.core.root import make_scheduled_calls
from albow.core.root import add_modifiers
from albow.core.root import make_due_calls
from albow.core.root import timestamp

from albow.core.root import set_modifier
from albow.core.root import Cancel
from albow.core.root import ApplicationError

import albow.media.music

MUSIC_END_EVENT = USEREVENT + 1

DOUBLE_CLICK_TIME = 300 # milliseconds

last_mouse_event = Event(0, pos = (0, 0), local = (0, 0))
last_mouse_event_handler = None

root_widget = None     # Root of the containment hierarchy

top_widget = None      # Initial dispatch target
clicked_widget = None  # Target of mouse_drag and mouse_up events
timer_event = None     # Timer event pending delivery
next_frame_due = 0.0   #

def get_top_widget():
    return top_widget


def get_focus():
    return top_widget.get_focus()

def get_root():
    return root_widget

class RootWidget(Widget):
    #
    #  surface   Pygame display surface
    #  is_gl     True if OpenGL surface

    redraw_every_frame = False
    do_draw            = False
    _is_gl_container   = True
    frame_time         = 0.0
    _use_sleep         = True

    def __init__(self, surface: Surface, **kwds):
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

            from albow.opengl import GLSurface
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
                #
                #  mouse_widget = None
                #  if clicked_widget:
                #  clicked_widget = modal_widget
                #
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
                        relative_warmup = 3     # Ignore spurious deltas on entering relative mode
                        # tb1 = timestamp() ###
                        # print "RootWidget: use_sleep =", use_sleep, "defer_drawing =", defer_drawing ###
                    if use_sleep and defer_drawing:
                        #  print "RootWidget: Handling timing" ###
                        time_now = timestamp()
                        #  print "RootWidget: Time is now", time_now ###
                        if next_frame_due < time_now:
                            #  print "RootWidget: Adjusting next frame due time to time now" ###
                            next_frame_due = time_now
                            #  print "RootWidget: Waiting for next frame due at", next_frame_due ###
                        while 1:
                            sleep_time = make_due_calls(time_now, next_frame_due)
                            if sleep_time <= 0.0:
                                break
                            # print "RootWidget: Sleeping for", sleep_time ###
                            sleep(sleep_time / 1000.0)
                            time_now = timestamp()
                        next_frame_due += self.frame_time
                        # print "RootWidget: Next frame now due at", next_frame_due ###
                        #
                        # Pygame 1.9 update
                        #
                        # timer_event = Event(USEREVENT, time = time_now)
                        timer_event = Event(USEREVENT, dict=None)
                        events = []
                    else:
                        events = [pygame.event.wait()]
                    # tb2 = timestamp() ###
                    # tb = tb2 - tb1 ###
                    # if tb: ###
                    # print "RootWidget: Event block %5d" % tb ###
                    events.extend(pygame.event.get())
                    for event in events:
                        t = timestamp()
                        event.dict['time'] = t
                        event.dict['local'] = getattr(event, 'pos', (0, 0))
                        eventType = event.type
                        if eventType == QUIT:
                            self.quit()
                        elif eventType == MOUSEBUTTONDOWN:
                            # print "RootWidget: MOUSEBUTTONDOWN: setting do_draw" ###
                            self.do_draw = True
                            if t - last_click_time <= DOUBLE_CLICK_TIME:
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
                                    #  modal_widget.dispatch_key('mouse_down', event)
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
                        elif eventType == MOUSEMOTION:
                            add_modifiers(event)
                            last_mouse_event = event
                            if in_relative_mode:
                                event.dict['local'] = (0, 0)
                                if not relative_pause:
                                    if relative_warmup:
                                        relative_warmup -= 1
                                    else:
                                        #  modal_widget.dispatch_key('mouse_delta', event)
                                        mouse_widget = clicked_widget or modal_widget.get_focus()
                                        last_mouse_event_handler = mouse_widget
                                        mouse_widget.handle_event('mouse_delta', event)
                            else:
                                mouse_widget = self.find_widget(event.pos)   # Do this in else branch?
                                if clicked_widget:
                                    last_mouse_event_handler = mouse_widget  # Should this be clicked_widget?
                                    clicked_widget.handle_mouse('mouse_drag', event)
                                else:
                                    if not mouse_widget.is_inside(modal_widget):
                                        mouse_widget = modal_widget
                                    last_mouse_event_handler = mouse_widget
                                    mouse_widget.handle_mouse('mouse_move', event)
                        elif eventType == MOUSEBUTTONUP:
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
                                #  mouse_widget = self.find_widget(event.pos) # Not necessary?
                                if clicked_widget:
                                    last_mouse_event_handler = clicked_widget
                                    clicked_widget = None
                                    last_mouse_event_handler.handle_mouse('mouse_up', event)
                        elif eventType == KEYDOWN:
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
                        elif eventType == KEYUP:
                            key = event.key
                            set_modifier(key, False)
                            self.do_draw = True
                            self.send_key(modal_widget, 'key_up', event)
                            if last_mouse_event_handler:
                                event.dict['pos'] = last_mouse_event.pos
                                event.dict['local'] = last_mouse_event.local
                                last_mouse_event_handler.setup_cursor(event)
                        elif eventType == MUSIC_END_EVENT:
                            self.music_end()
                        elif eventType == USEREVENT:
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

    def music_end(self):
        albow.media.music.music_end()

    def report_error(self, e):
        pass
