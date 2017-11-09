#!/usr/bin/env python3

import playerlib.config as config
from .mplayer import *

class BackendFactory:

    def __init__(self, context):
        self.context = context

    def create(self):
        backend_path = ''
        if config.backend == 'mplayer':
            try: backend_path = config.backend_path
            except: backend_path = 'mplayer'
            return MplayerBackend(self.context.playback_controller.next,
                self.context.player_controller.update_current_state, backend_path)
        else:
            raise RuntimeError('Improper backend name: ' + config.backend)

