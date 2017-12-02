#!/usr/bin/env python3

import urwid
import threading

from playerlib.bookmarks.bookmarks import *
from playerlib.command_handler import *
from playerlib.command_panel import *
from playerlib.file_browser.file_browser import *
from playerlib.helpers.asynchronous import AsyncCaller
from playerlib.main_view import *
from playerlib.playback_controller import *
from playerlib.player_context import *
from playerlib.player_view import *
from playerlib.playlist.playlist import *
from playerlib.track_info.track_info import *
from playerlib.user_input import *

class Loop(urwid.MainLoop):

    def __init__(self, draw_lock, *args, **kwargs):
        self.draw_lock = draw_lock
        super().__init__(*args, **kwargs)

    def draw_screen(self, *args, **kwargs):
        with self.draw_lock:
            super().draw_screen(*args, **kwargs)


class Player:

    def __init__(self, event_loop, screen, config):
        context = PlayerContext()
        self.context = context

        context.event_loop = event_loop
        context.quit = self.quit
        context.draw_lock = threading.RLock()
        context.config = config
        context.playback_controller = PlaybackController(context)
        context.command_handler = CommandHandler(context)
        context.command_panel = CommandPanel(context.command_handler)
        context.bookmarks = Bookmarks(context.config, context.command_handler)
        context.playlist = Playlist(context.playback_controller.play_track, context.command_handler)
        context.track_info = TrackInfo()
        context.file_browser = FileBrowser(context.command_handler)
        context.main_view = MainView(context.file_browser, context.bookmarks, context.playlist, context.track_info)
        context.view = PlayerView(context.main_view, context.command_panel)
        AsyncCaller(context.command_panel.error)

        self.main_loop = Loop(
            context.draw_lock,
            context.view,
            palette=context.config.color_palette,
            unhandled_input=UserInput(context).handle_input,
            event_loop=event_loop,
            screen=screen)


    def run(self):
        self.main_loop.run()
        self.context.playback_controller.quit()


    def quit(self):
        raise urwid.ExitMainLoop()

