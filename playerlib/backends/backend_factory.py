#!/usr/bin/env python3

from .mplayer import *

class BackendFactory:

    def __init__(self, config, play_next_track_callback, update_time_callback):
        self.config = config
        self.play_next_track_callback = play_next_track_callback
        self.update_time_callback = update_time_callback

    def create(self):
        if self.config.backend.name == 'mplayer':
            return MplayerBackend(self.play_next_track_callback, self.update_time_callback, self.config.backend.path)
        else:
            raise RuntimeError('Improper backend name: ' + self.config.backend.name)

