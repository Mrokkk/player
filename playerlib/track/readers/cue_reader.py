#!/usr/bin/env python3

import logging
import os
import re

from time import gmtime, strftime
from cueparser import *
from playerlib.track.track import *
from .tracks_reader_interface import *

class CueReader(TracksReaderInterface):

    def __init__(self):
        self._parser = CueParser()

    def _format_seconds_and_get_format_string(self, seconds):
        time_format = '%H:%M:%S' if seconds >= 3600 else '%M:%S'
        return strftime(time_format, gmtime(seconds)), time_format

    def read(self, path):
        cuesheet = self._parser.parse(path, use_taglib=True)
        tracks = []
        for t in cuesheet.tracks:
            new_track = Track()
            new_track.path = os.path.join(os.path.dirname(path), t.file)
            new_track.artist = ', '.join(cuesheet.title)
            new_track.title = ', '.join(t.title)
            new_track.index = str(t.index)
            new_track.length = t.length
            new_track.length_string, new_track.time_format = self._format_seconds_and_get_format_string(t.length)
            new_track.offset = t.offset
            tracks.append(new_track)
        return tracks

