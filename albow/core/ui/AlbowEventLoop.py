
from typing import List

import sys

import logging

from pygame.event import Event
from pygame.locals import MOUSEBUTTONDOWN
from pygame.locals import MOUSEBUTTONUP
from pygame.locals import MOUSEMOTION
from pygame.locals import K_ESCAPE
from pygame.locals import KMOD_CTRL
from pygame.locals import KMOD_SHIFT
from pygame.locals import KEYDOWN
from pygame.locals import KEYUP
from pygame.locals import USEREVENT
from pygame.locals import QUIT


from albow.core.Scheduler import Scheduler
from albow.core.CoreUtilities import CoreUtilities

from albow.core.ui.Widget import Widget
from albow.core.ui.RootWidget import RootWidget
from albow.core.ui.EventLoopParams import EventLoopParams

from albow.media.MusicUtilities import MusicUtilities


class AlbowEventLoop:

    MUSIC_END_EVENT = USEREVENT + 1
    """
    API consumer user events **MUST** start there events after this one
    """

    DOUBLE_CLICK_TIME = 300
    """
    Time is in milliseconds
    """

    def __init__(self, containingWidget: Widget, modalWidget: Widget):

        self.logger = logging.getLogger(__name__)
        self.modal_widget = modalWidget
        self.containingWidget = containingWidget

    def processEvents(self, eventList: List[Event], relativeMode: bool, deferDrawing: bool, eventLoopParams: EventLoopParams) -> EventLoopParams:

        self.logger.debug(f"Events to process: {len(eventList)}")


        use_sleep = eventLoopParams.use_sleep
        relative_pause = eventLoopParams.relative_pause
        do_draw = eventLoopParams.do_draw
        relative_warmup = eventLoopParams.relative_warmup
        last_click_time = eventLoopParams.last_click_time
        num_clicks = eventLoopParams.num_clicks

        for event in eventList:
            t = Scheduler.timestamp()
            event.dict['time'] = t
            event.dict['local'] = getattr(event, 'pos', (0, 0))
            eventType = event.type
            if eventType == QUIT:
                self.quit()
            elif eventType == MOUSEBUTTONDOWN:
                # print "RootWidget: MOUSEBUTTONDOWN: setting do_draw" ###
                do_draw = True
                if t - last_click_time <= AlbowEventLoop.DOUBLE_CLICK_TIME:
                    num_clicks += 1
                else:
                    num_clicks = 1
                last_click_time = t
                event.dict['num_clicks'] = num_clicks
                CoreUtilities.add_modifiers(event)
                RootWidget.last_mouse_event = event
                self.logger.debug(f"num_clicks: '{num_clicks}' -- t: '{t}' -- last_click_time: '{last_click_time}'")

                if relativeMode:
                    event.dict['local'] = (0, 0)
                    if relative_pause:
                        relative_pause = False
                    else:
                        #  modal_widget.dispatch_key('mouse_down', event)
                        mouse_widget = self.modal_widget.get_focus()
                        RootWidget.clicked_widget = mouse_widget
                        RootWidget.last_mouse_event_handler = mouse_widget
                        mouse_widget.handle_event('mouse_down', event)
                else:
                    mouse_widget = self.containingWidget.find_widget(event.pos)
                    if not mouse_widget.is_inside(self.modal_widget):
                        mouse_widget = self.modal_widget
                    RootWidget.clicked_widget = mouse_widget
                    RootWidget.last_mouse_event_handler = mouse_widget
                    mouse_widget.notify_attention_loss()
                    mouse_widget.handle_mouse('mouse_down', event)
            elif eventType == MOUSEMOTION:
                CoreUtilities.add_modifiers(event)
                RootWidget.last_mouse_event = event

                if relativeMode:
                    event.dict['local'] = (0, 0)
                    if not relative_pause:
                        if relative_warmup:
                            relative_warmup -= 1
                        else:
                            #  modal_widget.dispatch_key('mouse_delta', event)
                            mouse_widget = RootWidget.clicked_widget or self.modal_widget.get_focus()
                            RootWidget.last_mouse_event_handler = mouse_widget
                            mouse_widget.handle_event('mouse_delta', event)
                else:
                    mouse_widget = self.containingWidget.find_widget(event.pos)  # Do this in else branch?
                    if RootWidget.clicked_widget:
                        RootWidget.last_mouse_event_handler = mouse_widget  # Should this be clicked_widget?
                        RootWidget.clicked_widget.handle_mouse('mouse_drag', event)
                    else:
                        if not mouse_widget.is_inside(self.modal_widget):
                            mouse_widget = self.modal_widget
                        RootWidget.last_mouse_event_handler = mouse_widget
                        mouse_widget.handle_mouse('mouse_move', event)
            elif eventType == MOUSEBUTTONUP:
                CoreUtilities.add_modifiers(event)
                RootWidget.last_mouse_event = event
                do_draw = True
                if relativeMode:
                    event.dict['local'] = (0, 0)
                    if not relative_pause:

                        if RootWidget.clicked_widget:
                            mouse_widget = RootWidget.clicked_widget
                            RootWidget.clicked_widget = None
                        else:
                            mouse_widget = self.modal_widget.get_focus()
                        RootWidget.last_mouse_event_handler = mouse_widget
                        mouse_widget.handle_event('mouse_up', event)
                else:
                    if RootWidget.clicked_widget:
                        RootWidget.last_mouse_event_handler = RootWidget.clicked_widget
                        RootWidget.clicked_widget = None
                        RootWidget.last_mouse_event_handler.handle_mouse('mouse_up', event)
            elif eventType == KEYDOWN:
                key = event.key
                if key == K_ESCAPE and relativeMode and event.mod & KMOD_CTRL and event.mod & KMOD_SHIFT:
                    relative_pause = True
                elif relative_pause:
                    relative_pause = False
                else:
                    CoreUtilities.set_modifier(key, True)

                    do_draw = True
                    self.send_key(self.modal_widget, 'key_down', event)
                    if RootWidget.last_mouse_event_handler:
                        event.dict['pos'] = RootWidget.last_mouse_event.pos
                        event.dict['local'] = RootWidget.last_mouse_event.local
                        RootWidget.last_mouse_event_handler.setup_cursor(event)
            elif eventType == KEYUP:
                key = event.key
                CoreUtilities.set_modifier(key, False)

                do_draw = True
                self.send_key(self.modal_widget, 'key_up', event)
                if RootWidget.last_mouse_event_handler:
                    event.dict['pos'] = RootWidget.last_mouse_event.pos
                    event.dict['local'] = RootWidget.last_mouse_event.local
                    RootWidget.last_mouse_event_handler.setup_cursor(event)
            elif eventType == AlbowEventLoop.MUSIC_END_EVENT:
                self.music_end()
            elif eventType == USEREVENT:
                if deferDrawing and not use_sleep:
                    RootWidget.ourTimerEvent = event
            else:
                #
                # Maybe someone has registered some user events handler
                #
                userEventCallList = RootWidget.getUserEventList()
                for cb in userEventCallList:
                    if cb.userEvent == eventType:
                        self.logger.debug(f"API User eventType: {eventType}")
                        cb.func(event)

        retEventLoopParams: EventLoopParams = EventLoopParams(use_sleep=use_sleep,
                                                              relative_pause=relative_pause,
                                                              do_draw=do_draw,
                                                              relative_warmup=relative_warmup,
                                                              last_click_time=last_click_time,
                                                              num_clicks=num_clicks)

        return retEventLoopParams

    def send_key(self, theWidget: Widget, theName: str, theEvent: Event):

        CoreUtilities.add_modifiers(theEvent)
        theWidget.dispatch_key(theName, theEvent)

    def music_end(self):
        MusicUtilities.music_end()

    def quit(self):
        #
        # call quit handler
        sys.exit()
