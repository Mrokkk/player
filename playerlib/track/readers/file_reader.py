#!/usr/bin/env python3

import os
import taglib

from playerlib.track.track import *
from .tracks_reader_interface import *

class FileReader(TracksReaderInterface):

    extensions = [
        '.mp3', '.flac', '.m4a', '.wma', '.ogg', '.ape', '.alac', '.mpc', '.wav', '.wv'
    ]

    def _is_music_file(self, path):
        for e in self.extensions:
            if path.endswith(e): return True
        return False

    def read(self, path):
        if not self._is_music_file(path): return None
        track = Track()
        track.path = path
        tags = taglib.File(path)
        try: track.title = ', '.join(tags.tags['TITLE'])
        except KeyError: track.title = os.path.basename(path)
        try: track.artist = ', '.join(tags.tags['ARTIST'])
        except KeyError: pass
        try: track.index = tags.tags['TRACKNUMBER'][0]
        except KeyError: pass
        track.length = tags.length
        track.length_string, track.time_format = self._format_seconds_and_get_format_string(track.length)
        return [track]

