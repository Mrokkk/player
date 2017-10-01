#!/usr/bin/env python3

import urwid

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

class Player:

    def __init__(self, event_loop, screen):
        context = PlayerContext()

        player_controller = PlayerController(context)
        context.player_controller = player_controller

        self.playback_controller = PlaybackController(player_controller.update_current_state)
        context.playback_controller = self.playback_controller

        command_handler = CommandHandler(context)
        context.command_handler = command_handler

        command_panel = CommandPanel(command_handler)
        context.command_panel = command_panel

        playlist = Playlist(self.playback_controller.play_file, player_controller.error_handler)
        context.playlist = playlist

        file_browser = FileBrowser(player_controller.add_to_playlist, player_controller.error_handler)

        context.view = PlayerView(file_browser, playlist, command_panel)

        self.main_loop = urwid.MainLoop(
            context.view,
            palette=config.color_palette,
            unhandled_input=UserInput(context.view, command_handler, command_panel, player_controller.error_handler)
                .handle_input,
            event_loop=urwid.AsyncioEventLoop(loop=event_loop),
            screen=screen)

    def run(self):
        self.main_loop.run()
        self.playback_controller.quit()

