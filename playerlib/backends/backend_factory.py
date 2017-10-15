#!/usr/bin/env python3

import playerlib.config as config
from .mplayer import *

class BackendFactory:

    def __init__(self, context):
        self.context = context

    def create(self):
        if config.backend == 'mplayer':
            return MplayerBackend(self.context.playback_controller.next,
                self.context.player_controller.update_current_state)
        else:
            raise RuntimeError('Improper backend name: ' + config.backend)

