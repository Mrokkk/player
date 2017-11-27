#!/usr/bin/env python3

import fnmatch
import os
import re
import taglib
from time import gmtime, strftime

from playerlib.track import *
from playerlib.cue_parser import *

class TracksFactory:

    extensions = [
        '.mp3', '.flac', '.m4a', '.wma', '.ogg', '.ape', '.alac', '.mpc', '.wav', '.wv'
    ]

    def _is_music_file(self, path):
        for e in self.extensions:
            if path.endswith(e): return True
        return False

    def _format_seconds_and_get_format_string(self, seconds):
        time_format = '%H:%M:%S' if seconds >= 3600 else '%M:%S'
        return strftime(time_format, gmtime(seconds)), time_format

    def _handle_cue_sheet(self, path):
        cuesheet = CueParser().parse(path, use_taglib=True)
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

    def _handle_file(self, path):
        if not self._is_music_file(path): return None
        track = Track()
        track.path = path
        tags = taglib.File(path)
        try:
            track.title = ', '.join(tags.tags['TITLE'])
        except KeyError: pass
        try:
            track.artist = ', '.join(tags.tags['ARTIST'])
        except KeyError: pass
        try:
            track.index = tags.tags['TRACKNUMBER'][0]
        except KeyError: pass
        track.length = tags.length
        track.length_string, track.time_format = self._format_seconds_and_get_format_string(track.length)
        return track

    def _predicate(self, f):
        if f[0].isdigit():
            a = re.search('[0-9]+', f).group(0)
            return a.zfill(9)
        return f

    def _handle_dir(self, path):
        cue_files = fnmatch.filter([os.path.join(path, x) for x in os.listdir(path)], '*.cue')
        if len(cue_files) == 0:
            return [self._handle_file(os.path.join(path, f))
                for f in sorted(os.listdir(path), key=self._predicate)
                    if os.path.isfile(os.path.join(path, f)) and self._is_music_file(f)]
        tracks = []
        for cue in cue_files:
            tracks.extend(self._handle_cue_sheet(cue))
        return tracks

    def _handle_cdda(self):
        try:
            import discid
        except:
            raise RuntimeError('Cannot import discid. Is it installed?')
        device_name = discid.get_default_device()
        disc = discid.read(device_name)
        tracks = []
        for cdda_track in disc.tracks:
            track = Track()
            track.path = 'cdda://'
            track.title = 'CD Audio track' # TODO: read tags from FreeDB
            track.index = cdda_track.number
            track.length = cdda_track.seconds
            track.length_string, track.time_format = self._format_seconds_and_get_format_string(track.length)
            try:
                track.offset = tracks[-1].offset + tracks[-1].length
            except:
                pass
            tracks.append(track)
        return tracks

    def get(self, path):
        if path == 'cdda://':
            return self._handle_cdda()
        elif os.path.isfile(path):
            if path.endswith('.cue'): return self._handle_cue_sheet(path)
            f = self._handle_file(path)
            if f: return [f]
        elif os.path.isdir(path):
            return self._handle_dir(path)

