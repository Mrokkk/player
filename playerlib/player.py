#!/usr/bin/env python3

from playerlib.helpers.app import *
from playerlib.helpers.vertical_box import *

from playerlib.bookmarks.bookmarks import *
from playerlib.commands import *
from playerlib.config import *
from playerlib.context import *
from playerlib.file_browser.file_browser import *
from playerlib.playback_controller import *
from playerlib.playlist.playlist import *
from playerlib.track_info.track_info import *


class Player:

    keys_mapping = {
        'h': ':seek -10',
        'l': ':seek +10',
        'H': ':seek -60',
        'L': ':seek +60',
        ' ': ':pause',
        '[': ':set volume -10',
        ']': ':set volume +10',
    }

    def __init__(self):
        context = Context()
        self.context = context

        context.config = Config()
        context.playback_controller = PlaybackController(context)
        context.bookmarks = Bookmarks(context.config)
        context.playlist = Playlist(context.playback_controller.play_track)
        context.track_info = TrackInfo()
        context.file_browser = FileBrowser()
        main_view = VerticalBox([[context.file_browser, context.bookmarks],
            [context.playlist, context.track_info]])

        self.app = App(
            main_view,
            commands=Commands(context),
            keys_mapping=self.keys_mapping,
            palette=context.config.color_palette)

        # TODO: remove
        context.draw_lock = App().draw_lock
        context.command_panel = self.app.command_panel
        context.command_handler = self.app.command_handler


    def run(self):
        self.app.run()
        self.context.playback_controller.quit()

