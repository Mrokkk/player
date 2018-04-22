#!/usr/bin/env python3

import fnmatch
import os
import re
import taglib
from time import gmtime, strftime

from playerlib.track.readers.cdaudio_reader import *
from playerlib.track.readers.cue_reader import *
from playerlib.track.readers.file_reader import *
from playerlib.track.track import *

class TracksReader:

    def __init__(self):
        self._cdaudio_reader = CdaudioReader()
        self._cue_reader = CueReader()
        self._file_reader = FileReader()

    def _predicate(self, f):
        if f[0].isdigit():
            a = re.search('[0-9]+', f).group(0)
            return a.zfill(9)
        return f

    def _handle_dir(self, path):
        cue_files = fnmatch.filter([os.path.join(path, x) for x in os.listdir(path)], '*.cue')
        if len(cue_files) == 0:
            tracks = []
            for f in sorted(os.listdir(path), key=self._predicate):
                if not os.path.isfile(os.path.join(path, f)): continue
                track = self._file_reader.read(os.path.join(path, f))
                if track: tracks.append(track[0])
            return tracks
        tracks = []
        for cue in cue_files:
            tracks.extend(self._cue_reader.read(cue))
        return tracks

    def read(self, path):
        if path == 'cdda://':
            return self._cdaudio_reader.read(path)
        elif os.path.isfile(path):
            if path.endswith('.cue'): return self._cue_reader.read(path)
            return self._file_reader.read(path)
        elif os.path.isdir(path):
            return self._handle_dir(path)

