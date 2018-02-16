#!/usr/bin/env python3

import urwim

from playerlib.bookmarks.bookmarks import *
from playerlib.commands import *
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

    default_config = {
        'backend': {'name': 'mplayer', 'path': '/usr/bin/mplayer'},
        'bookmarks': {'path': '~/.config/player/bookmarks.json'},
    }

    def __init__(self):
        context = Context()
        context.config = urwim.read_config(config_files=['~/.config/player/config.json', '~/.config/player/config.yml'],
            defaults=self.default_config)
        context.playback_controller = PlaybackController(context.config)
        context.bookmarks = Bookmarks(context.config)
        context.playlist = Playlist(context.playback_controller.play_track)
        context.track_info = TrackInfo()
        context.file_browser = FileBrowser()
        self.context = context

        self.app = urwim.App(
            urwim.VerticalBox([[context.file_browser, context.bookmarks],
                [context.playlist, context.track_info]]),
            commands=Commands(context),
            keys_mapping=self.keys_mapping,
            command_mapping={'e': 'add_to_playlist'},
            palette=context.config.color_palette)


    def run(self):
        self.app.run()
        self.context.playback_controller.quit()

