#!/usr/bin/env python3

from .mplayer import *

class BackendFactory:

    def __init__(self):
        pass

    def create(self, config, next, update_current_state):
        backend_path = ''
        if config.backend == 'mplayer':
            return MplayerBackend(next,
                update_current_state, config.backend_path)
        else:
            raise RuntimeError('Improper backend name: ' + config.backend)

