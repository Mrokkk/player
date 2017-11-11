#!/usr/bin/env python3

import urwid
import threading

from playerlib.backends.backend_factory import *
from playerlib.command_handler import *
from playerlib.command_panel import *
from playerlib.config import *
from playerlib.file_browser.file_browser import *
from playerlib.playback_controller import *
from playerlib.player_context import *
from playerlib.player_controller import *
from playerlib.player_view import *
from playerlib.playlist.playlist import *
from playerlib.user_input import *

class Loop(urwid.MainLoop):

    def __init__(self, draw_lock, *args, **kwargs):
        self.draw_lock = draw_lock
        super().__init__(*args, **kwargs)

    def draw_screen(self, *args, **kwargs):
        with self.draw_lock:
            super().draw_screen(*args, **kwargs)


class Player:

    def __init__(self, event_loop, screen):

        context = PlayerContext()
        self.context = context

        context.draw_lock = threading.RLock()
        context.config = Config()
        context.player_controller = PlayerController(context)
        context.playback_controller = PlaybackController(BackendFactory(context))
        context.command_handler = CommandHandler(context)
        context.command_panel = CommandPanel(context.command_handler)
        error_handler = context.command_panel.error
        context.playlist = Playlist(context.playback_controller.play_track, error_handler)
        context.file_browser = FileBrowser(context.playlist.add_to_playlist, error_handler)
        context.view = PlayerView(context.file_browser, context.playlist, context.command_panel)

        self.main_loop = Loop(
            context.draw_lock,
            context.view,
            palette=context.config.color_palette,
            unhandled_input=UserInput(context.view, context.command_handler, context.command_panel, error_handler)
                .handle_input,
            event_loop=event_loop,
            screen=screen)

    def run(self):
        self.main_loop.run()
        self.context.playback_controller.quit()

