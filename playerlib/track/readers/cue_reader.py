#!/usr/bin/env python3

import logging
import os
import re

from cueparser import *
from playerlib.track.track import *
from .tracks_reader_interface import *

class CueReader(TracksReaderInterface):

    def __init__(self):
        self._parser = CueParser()

    def read(self, path):
        if not path.endswith('.cue'): return None
        cuesheet = self._parser.parse(path, use_taglib=True)
        tracks = []
        for t in cuesheet.tracks:
            new_track = Track()
            new_track.path = os.path.join(os.path.dirname(path), t.file)
            new_track.artist = cuesheet.title
            new_track.title = t.title
            new_track.index = str(t.index)
            new_track.length = t.length
            new_track.length_string, new_track.time_format = self._format_seconds_and_get_format_string(t.length)
            new_track.offset = t.offset
            tracks.append(new_track)
        return tracks

