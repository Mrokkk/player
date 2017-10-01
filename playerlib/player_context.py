#!/usr/bin/env python3

class PlayerContext:

    def __init__(self, panes, playlist, file_browser, playback_controller, tracks_factory, player):
        self.panes = panes
        self.playlist = playlist
        self.file_browser = file_browser
        self.playback_controller = playback_controller
        self.tracks_factory = tracks_factory
        self.player = player

