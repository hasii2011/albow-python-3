
from typing import List

import sys

from time import sleep

import logging
from logging import Logger


import pygame
from pygame.mouse import set_visible as set_mouse_visible
from pygame.time import set_timer as set_pygame_timer

from pygame import Surface

from pygame.event import Event
from pygame.event import get_grab
from pygame.event import set_grab

from pygame.locals import USEREVENT
from pygame.locals import OPENGL

from albow.core.ui.Widget import Widget

from albow.core.Scheduler import Scheduler
from albow.core.CoreUtilities import CoreUtilities
from albow.core.exceptions.CancelException import CancelException
from albow.core.exceptions.ApplicationException import ApplicationException

from albow.core.UserEventCall import UserEventCall

from albow.media.MusicUtilities import MusicUtilities


class RootWidget(Widget):


    """
    For the GUI to function, there must be exactly one instance of RootWidget. It implements the main event loop
    and serves as the ultimate container for all other visible widgets.

    The root widget can be found using the `RootWidget.get_root()`

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

    # redraw_every_frame = False
    # """
    # If true, all widgets will be redrawn on every animation frame (i.e. after every call to begin_frame()). If false,
    # redrawing only occurs after user input events, such as mouse clicks and keystrokes, or if a widget calls
    # its invalidate() method. The default is false.
    # """
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

    classLogger: Logger
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

        RootWidget.classLogger = logging.getLogger(__name__)
        CoreUtilities.init_timebase()
        self.surface = surface
        RootWidget.root_widget = self
        Widget.root_widget = self

        self.is_gl = surface.get_flags() & OPENGL != 0
        # RootWidget.classLogger.info(f"self.is_gl: {self.is_gl}")
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

            self.do_draw = True
            use_sleep = self._use_sleep

            from albow.core.ui.AlbowEventLoop import AlbowEventLoop
            from albow.core.ui.EventLoopParams import EventLoopParams

            eventLoop: AlbowEventLoop = AlbowEventLoop(modalWidget=modal_widget, containingWidget=self)

            last_click_time = 0
            num_clicks = 0
            while modal_widget.modal_result is None:

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
                                self.do_draw = False
                    # RootWidget.classLogger.info(f"self.do_draw: {self.do_draw}")
                    if self.do_draw:
                        if self.is_gl:
                            gl_surface = self.gl_surface
                            gl_surface.gl_clear(self.bg_color)
                            self.gl_draw_all(gl_surface)
                            gl_surface.gl_flush()
                        else:
                            self.draw_all(self.surface)
                        self.do_draw = False
                        # tb1 = timestamp() ###
                        pygame.display.flip()

                    in_relative_mode = bool(modal_widget.relative_mode())
                    grab = in_relative_mode and not relative_pause
                    if grab != get_grab():
                        set_grab(grab)
                        set_mouse_visible(not grab)
                        relative_warmup = 3            # Ignore spurious deltas on entering relative mode
                    if use_sleep and defer_drawing:

                        time_now = Scheduler.timestamp()

                        if RootWidget.nextFrameDue < time_now:
                            RootWidget.nextFrameDue = time_now

                        while True:
                            sleep_time = Scheduler.make_due_calls(time_now, RootWidget.nextFrameDue)
                            if sleep_time <= 0.0:
                                break

                            sleep(sleep_time / 1000.0)
                            time_now = Scheduler.timestamp()
                        RootWidget.nextFrameDue += self.frame_time
                        RootWidget.ourTimerEvent = Event(USEREVENT, {'time': time_now})
                        events = []
                    else:
                        events = [pygame.event.wait()]
                    events.extend(pygame.event.get())

                    loopParams: EventLoopParams = EventLoopParams(use_sleep=use_sleep, relative_pause=relative_pause, do_draw=self.do_draw,
                                                                  relative_warmup=relative_warmup, last_click_time=last_click_time,
                                                                  num_clicks=num_clicks)

                    newParams: EventLoopParams = eventLoop.processEvents(eventList=events, relativeMode=in_relative_mode, deferDrawing=defer_drawing,
                                                                         eventLoopParams=loopParams)

                    use_sleep = newParams.use_sleep
                    relative_pause = newParams.relative_pause
                    self.do_draw = newParams.do_draw
                    relative_warmup = newParams.relative_warmup
                    last_click_time = newParams.last_click_time
                    num_clicks = newParams.num_clicks

                except CancelException:
                    pass

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

    @classmethod
    def addUserEvent(cls, newCallback: UserEventCall):

        cls.userEventCallList.append(newCallback)
        cls.classLogger.debug(f"add - userEventListSize: {len(cls.userEventCallList)}")

    @classmethod
    def getUserEventList(cls):
        cls.classLogger.debug(f"get - userEventListSize: {len(cls.userEventCallList)}")
        return cls.userEventCallList

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
