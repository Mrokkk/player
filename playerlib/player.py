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

    default_config = {
        'backend': {'name': 'mplayer', 'path': '/usr/bin/mplayer'},
        'bookmarks': {'path': '~/.config/player/bookmarks.json'},
        'keys_mapping': {
            'h': ':seek -10',
            'l': ':seek +10',
            'H': ':seek -60',
            'L': ':seek +60',
            ' ': ':pause',
            '[': ':set volume -10',
            ']': ':set volume +10',
        },
        'commands_mapping': {
            'e': 'add_to_playlist'
        }
    }

    def __init__(self, verbose=False):
        context = Context()
        commands = Commands(context)
        context.config = urwim.read_config(config_files=['~/.config/player/config.json', '~/.config/player/config.yml'],
            defaults=self.default_config)
        urwim.read_persistent_data('~/.player')
        context.playback_controller = PlaybackController(context.config)
        context.playlist = Playlist(context.playback_controller.play_track)
        context.file_browser = FileBrowser(commands)
        context.bookmarks = Bookmarks(context.config, commands)
        context.track_info = TrackInfo()
        self.context = context
        widget = urwim.VerticalBox([
            [context.file_browser, context.bookmarks],
            [context.playlist, context.track_info]
        ])

        self.app = urwim.App(
            widget,
            context.config,
            commands=commands,
            log_exceptions=verbose)


    def run(self):
        self.app.run()
        self.context.playback_controller.quit()

