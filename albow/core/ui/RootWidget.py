
from typing import List

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

from albow.core.ui.Widget import Widget
from albow.core.Scheduler import Scheduler
from albow.core.CoreUtilities import CoreUtilities
from albow.core.exceptions.CancelException import CancelException
from albow.core.exceptions.ApplicationException import ApplicationException

from albow.core.UserEventCall import UserEventCall

from albow.media.MusicUtilities import MusicUtilities


class RootWidget(Widget):

    DOUBLE_CLICK_TIME = 300
    """
    Time is in milliseconds
    """

    """
    For the GUI to function, there must be exactly one instance of RootWidget. It implements the main event loop
    and serves as the ultimate container for all other visible widgets.

    The root widget can be found using the `RootWidget.get_root()`

    """
    MUSIC_END_EVENT = USEREVENT + 1
    """
    API consumer user events **MUST** start there events after this one
    """

    root_widget = None
    """
    Root of the containment hierarchy
    """
    top_widget = None
    """
    Initial dispatch target
    """
    clicked_widget = None
    """
    Target of mouse_drag and mouse_up events
    """

    redraw_every_frame = False
    """
    If true, all widgets will be redrawn on every animation frame (i.e. after every call to begin_frame()). If false, 
    redrawing only occurs after user input events, such as mouse clicks and keystrokes, or if a widget calls 
    its invalidate() method. The default is false.
    """
    last_mouse_event_handler = None

    ourTimerEvent = None
    """
    Timer event pending delivery
    """
    nextFrameDue = 0.0

    do_draw          = False
    _is_gl_container = True
    frame_time       = 0.0
    _use_sleep       = True

    last_mouse_event: Event = Event(0, {'pos': (0, 0), 'local': (0, 0)})

    userEventCallList: List = []

    def __init__(self, surface: Surface, **kwds):
        """
        Initializes the root widget with the given surface, which will normally be the PyGame screen,
        but could be a subsurface of it.

        Args:
            surface:  A Pygame surface

            **kwds:
        """
        super().__init__(surface.get_rect(), **kwds)

        print(f"__name__: '{__name__}'")
        CoreUtilities.init_timebase()
        self.surface = surface
        RootWidget.root_widget = self
        Widget.root_widget = self
        #
        # Python 3 update
        #
        # self.is_gl = surface.get_flags() & OPENGL <> 0
        self.is_gl = surface.get_flags() & OPENGL != 0
        if self.is_gl:

            from albow.openGL.GLSurface import GLSurface
            self.gl_surface = GLSurface(surface, self.rect)

    def set_timer(self, ms):
        """
        Arranges for timer events to be generated every interval milliseconds. See timer_event().

        Args:
            ms:  The timer interval in milli-seconds

        """
        self.frame_time = ms
        if not self._use_sleep:
            set_pygame_timer(USEREVENT, max(1, int(round(ms))))

    def run(self):
        """
        Runs the main event loop. Control is retained until a QUIT event is received, whereupon the quit() method
        is called.

        """
        self.run_modal(None)

    def run_modal(self, modal_widget: Widget):
        """
            Runs a modal event loop. The widget is run as a modal dialog until its dismiss() method is called.
        Args:
            modal_widget:  The modal widget
        """
        is_modal = modal_widget is not None
        modal_widget = modal_widget or self
        relative_pause = False
        relative_warmup = 0

        was_modal = None
        try:
            RootWidget.old_top_widget = RootWidget.top_widget
            RootWidget.top_widget = modal_widget
            was_modal = modal_widget.is_modal

            modal_widget.is_modal = True
            modal_widget.modal_result = None
            if not modal_widget.focus_switch:
                modal_widget.tab_to_first()

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
                        if RootWidget.ourTimerEvent:
                            if not use_sleep and defer_drawing:
                                Scheduler.make_scheduled_calls()
                            CoreUtilities.add_modifiers(RootWidget.ourTimerEvent)
                            if RootWidget.last_mouse_event:
                                RootWidget.ourTimerEvent.dict['pos'] = RootWidget.last_mouse_event.pos
                                RootWidget.ourTimerEvent.dict['local'] = RootWidget.last_mouse_event.local
                            if RootWidget.last_mouse_event_handler:
                                RootWidget.last_mouse_event_handler.setup_cursor(RootWidget.ourTimerEvent)
                            self.do_draw = self.timer_event(RootWidget.ourTimerEvent)
                            RootWidget.ourTimerEvent = None
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
                        time_now = Scheduler.timestamp()
                        #  print "RootWidget: Time is now", time_now ###
                        if RootWidget.nextFrameDue < time_now:
                            #  print "RootWidget: Adjusting next frame due time to time now" ###
                            RootWidget.nextFrameDue = time_now
                            #  print "RootWidget: Waiting for next frame due at", next_frame_due ###
                        while 1:
                            sleep_time = Scheduler.make_due_calls(time_now, RootWidget.nextFrameDue)
                            if sleep_time <= 0.0:
                                break
                            # print "RootWidget: Sleeping for", sleep_time ###
                            sleep(sleep_time / 1000.0)
                            time_now = Scheduler.timestamp()
                        RootWidget.nextFrameDue += self.frame_time
                        # print "RootWidget: Next frame now due at", next_frame_due ###
                        #
                        # Pygame 1.9 update
                        #
                        # timer_event = Event(USEREVENT, time = time_now)
                        RootWidget.ourTimerEvent = Event(USEREVENT, {'time': time_now})
                        events = []
                    else:
                        events = [pygame.event.wait()]
                    # tb2 = timestamp() ###
                    # tb = tb2 - tb1 ###
                    # if tb: ###
                    # print "RootWidget: Event block %5d" % tb ###
                    events.extend(pygame.event.get())
                    for event in events:
                        t = Scheduler.timestamp()
                        event.dict['time'] = t
                        event.dict['local'] = getattr(event, 'pos', (0, 0))
                        eventType = event.type
                        if eventType == QUIT:
                            self.quit()
                        elif eventType == MOUSEBUTTONDOWN:
                            # print "RootWidget: MOUSEBUTTONDOWN: setting do_draw" ###
                            self.do_draw = True
                            if t - last_click_time <= RootWidget.DOUBLE_CLICK_TIME:
                                num_clicks += 1
                            else:
                                num_clicks = 1
                            last_click_time = t
                            event.dict['num_clicks'] = num_clicks
                            CoreUtilities.add_modifiers(event)
                            RootWidget.last_mouse_event = event
                            if in_relative_mode:
                                event.dict['local'] = (0, 0)
                                if relative_pause:
                                    relative_pause = False
                                else:
                                    #  modal_widget.dispatch_key('mouse_down', event)
                                    mouse_widget = modal_widget.get_focus()
                                    RootWidget.clicked_widget = mouse_widget
                                    RootWidget.last_mouse_event_handler = mouse_widget
                                    mouse_widget.handle_event('mouse_down', event)
                            else:
                                mouse_widget = self.find_widget(event.pos)
                                if not mouse_widget.is_inside(modal_widget):
                                    mouse_widget = modal_widget
                                RootWidget.clicked_widget = mouse_widget
                                RootWidget.last_mouse_event_handler = mouse_widget
                                mouse_widget.notify_attention_loss()
                                mouse_widget.handle_mouse('mouse_down', event)
                        elif eventType == MOUSEMOTION:
                            CoreUtilities.add_modifiers(event)
                            RootWidget.last_mouse_event = event
                            if in_relative_mode:
                                event.dict['local'] = (0, 0)
                                if not relative_pause:
                                    if relative_warmup:
                                        relative_warmup -= 1
                                    else:
                                        #  modal_widget.dispatch_key('mouse_delta', event)
                                        mouse_widget = RootWidget.clicked_widget or modal_widget.get_focus()
                                        RootWidget.last_mouse_event_handler = mouse_widget
                                        mouse_widget.handle_event('mouse_delta', event)
                            else:
                                mouse_widget = self.find_widget(event.pos)   # Do this in else branch?
                                if RootWidget.clicked_widget:
                                    RootWidget.last_mouse_event_handler = mouse_widget  # Should this be clicked_widget?
                                    RootWidget.clicked_widget.handle_mouse('mouse_drag', event)
                                else:
                                    if not mouse_widget.is_inside(modal_widget):
                                        mouse_widget = modal_widget
                                    RootWidget.last_mouse_event_handler = mouse_widget
                                    mouse_widget.handle_mouse('mouse_move', event)
                        elif eventType == MOUSEBUTTONUP:
                            CoreUtilities.add_modifiers(event)
                            RootWidget.last_mouse_event = event
                            self.do_draw = True
                            if in_relative_mode:
                                event.dict['local'] = (0, 0)
                                if not relative_pause:

                                    if RootWidget.clicked_widget:
                                        mouse_widget = RootWidget.clicked_widget
                                        RootWidget.clicked_widget = None
                                    else:
                                        mouse_widget = modal_widget.get_focus()
                                    RootWidget.last_mouse_event_handler = mouse_widget
                                    mouse_widget.handle_event('mouse_up', event)
                            else:
                                if RootWidget.clicked_widget:
                                    RootWidget.last_mouse_event_handler = RootWidget.clicked_widget
                                    RootWidget.clicked_widget = None
                                    RootWidget.last_mouse_event_handler.handle_mouse('mouse_up', event)
                        elif eventType == KEYDOWN:
                            key = event.key
                            if key == K_ESCAPE and in_relative_mode and \
                                    event.mod & KMOD_CTRL and event.mod & KMOD_SHIFT:
                                relative_pause = True
                            elif relative_pause:
                                relative_pause = False
                            else:
                                CoreUtilities.set_modifier(key, True)
                                self.do_draw = True
                                self.send_key(modal_widget, 'key_down', event)
                                if RootWidget.last_mouse_event_handler:
                                    event.dict['pos'] = RootWidget.last_mouse_event.pos
                                    event.dict['local'] = RootWidget.last_mouse_event.local
                                    RootWidget.last_mouse_event_handler.setup_cursor(event)
                        elif eventType == KEYUP:
                            key = event.key
                            CoreUtilities.set_modifier(key, False)
                            self.do_draw = True
                            self.send_key(modal_widget, 'key_up', event)
                            if RootWidget.last_mouse_event_handler:
                                event.dict['pos'] = RootWidget.last_mouse_event.pos
                                event.dict['local'] = RootWidget.last_mouse_event.local
                                RootWidget.last_mouse_event_handler.setup_cursor(event)
                        elif eventType == RootWidget.MUSIC_END_EVENT:
                            self.music_end()
                        elif eventType == USEREVENT:
                            if defer_drawing and not use_sleep:
                                RootWidget.ourTimerEvent = event
                        else:
                            #
                            # Maybe someone has registered some user events handler
                            #
                            for cb in RootWidget.userEventCallList:
                                if cb.userEvent == eventType:
                                    self.logger.debug(f"API User eventType: {eventType}")
                                    cb.func(event)

                except CancelException:
                    pass
                #
                # Python 3 update
                #
                # except ApplicationError, e:
                except ApplicationException as e:
                    self.report_error(e)
        finally:
            modal_widget.is_modal = was_modal
            RootWidget.top_widget = RootWidget.old_top_widget

        RootWidget.clicked_widget = None

    def send_key(self, widget, name, event):
        CoreUtilities.add_modifiers(event)
        widget.dispatch_key(name, event)

    def begin_frame(self):
        """Deprecated, use timer_event() instead."""
        pass

    def has_focus(self):
        return True

    def quit(self):
        """
        This method is called when a QUIT event is received. The default implementation first calls
        confirm_quit(), and if it returns true, calls sys.exit(0).
        """
        if self.confirm_quit():
            sys.exit(0)

    def get_mouse_for(self, widget):
        last = RootWidget.last_mouse_event
        event = Event(0, last.dict)
        event.dict['local'] = widget.global_to_local(event.pos)
        CoreUtilities.add_modifiers(event)
        return event

    def music_end(self):
        MusicUtilities.music_end()

    @staticmethod
    def getRoot():
        """
        Returns:  The root widget of the containment hierarchy
        """
        return RootWidget.root_widget

    @staticmethod
    def getTopWidget():
        return RootWidget.top_widget

    @staticmethod
    def getFocus():
        return RootWidget.top_widget.get_focus()

    @staticmethod
    def addUserEvent(newCallback: UserEventCall):

        RootWidget.userEventCallList.append(newCallback)

    # ========================================================================
    #
    #  Abstract methods follow
    #
    # ========================================================================

    def report_error(self, e):
        pass

    def confirm_quit(self) -> bool:
        """
        Called to give an opportunity to ask the user to confirm quitting the main event loop. If it returns
        true, sys.exit(0) is performed, otherwise nothing is done. The default implementation unconditionally
        returns true.

        Returns: True to confirm else False

        """
        return True

    def defer_drawing(self) -> bool:
        """
        f this method returns true, pending display updates are only performed when a timer event occurs and the
        timer_event() method of the root widget returns true. Otherwise, the display is updated after every input
        event except for mouse-move events. The default implementation returns True.

        Returns: True to defer else False

        """
        return True

    def timer_event(self, event):
        """
        Called when a timer event occurs. See set_timer(). If it returns true, a display update is performed. The
        default implementation returns true.

        Note:
            If multiple timer events occur during a single pass through the event loop, only the most recent
            one is passed to timer_event() and the others are discarded. Also, if other types of event occur during
            the same pass through the event loop, all the other events are processed before calling timer_event(), even
            if the timer event was not the last to occur chronologically.

        Args:
            event:

        Returns:  True

        """
        self.begin_frame()
        return True
