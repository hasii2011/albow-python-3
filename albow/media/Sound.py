"""
The sound module exports  utility functions related to sound. These functions have the property that
if sound support is not available, they do nothing, allowing an application to continue without sound.
"""
import pygame
from pygame import mixer


def pause_sound():
    """
    Pauses all sound channels. Equivalent to `pygame.mixer.pause()`.
    """
    try:
        mixer.pause()
    except pygame.error:
        pass


def resume_sound():
    """
    Resumes channels previously paused by `pause_sound()`. Equivalent to `pygame.mixer.unpause().`
    """
    try:
        mixer.unpause()
    except pygame.error:
        pass


def stop_sound():
    """
    Stops all sound channels. Equivalent to `pygame.mixer.stop()`.
    """
    try:
        mixer.stop()
    except pygame.error:
        pass
