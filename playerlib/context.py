#!/usr/bin/env python3

from typing import Any

from playerlib.bookmarks.bookmarks import *
from playerlib.file_browser.file_browser import *
from playerlib.playback_controller import *
from playerlib.track_info.track_info import *

class Context:

    bookmarks:           Bookmarks
    config:              dict[str, str | Any]
    file_browser:        FileBrowser
    playback_controller: PlaybackController
    track_info:          TrackInfo

    def __init__(self):
        self.bookmarks = None
        self.config = None
        self.file_browser = None
        self.playback_controller = None
        self.playlist = None
        self.track_info = None

