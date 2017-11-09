#!/usr/bin/env python3

import urwid
import threading

import playerlib.config as config
from playerlib.command_handler import *
from playerlib.command_panel import *
from playerlib.file_browser.file_browser import *
from playerlib.playback_controller import *
from playerlib.player_context import *
from playerlib.player_controller import *
from playerlib.player_view import *
from playerlib.playlist.playlist import *
from playerlib.user_input import *
from playerlib.backends.backend_factory import *

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
        context.draw_lock = threading.RLock()

        player_controller = PlayerController(context)
        context.player_controller = player_controller

        self.playback_controller = PlaybackController(BackendFactory(context))
        context.playback_controller = self.playback_controller

        command_handler = CommandHandler(context)
        context.command_handler = command_handler

        command_panel = CommandPanel(command_handler)
        context.command_panel = command_panel

        error_handler = context.command_panel.error

        playlist = Playlist(self.playback_controller.play_track, error_handler)
        context.playlist = playlist

        file_browser = FileBrowser(playlist.add_to_playlist, error_handler)
        context.file_browser = file_browser

        context.view = PlayerView(file_browser, playlist, command_panel)

        self.main_loop = Loop(
            context.draw_lock,
            context.view,
            palette=config.color_palette,
            unhandled_input=UserInput(context.view, command_handler, command_panel, error_handler)
                .handle_input,
            event_loop=urwid.AsyncioEventLoop(loop=event_loop),
            screen=screen)

    def run(self):
        self.main_loop.run()
        self.playback_controller.quit()

