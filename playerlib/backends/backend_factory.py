#!/usr/bin/env python3

from .mplayer import *

class BackendFactory:

    def __init__(self, context):
        self.context = context

    def create(self):
        backend_path = ''
        if self.context.config.backend == 'mplayer':
            return MplayerBackend(self.context.playback_controller.next,
                self.context.player_controller.update_current_state, self.context.config.backend_path)
        else:
            raise RuntimeError('Improper backend name: ' + self.context.config.backend)

