#!/usr/bin/env python3

import cueparser
import discid
import glob
import os
import re
import taglib

from playerlib.track import *

class TracksFactory:

    extensions = [
        '.mp3', '.flac', '.m4a', '.wma', '.ogg', '.ape', '.alac', '.mpc', '.wav', '.wv'
    ]

    def _is_music_file(self, path):
        for e in self.extensions:
            if path.endswith(e): return True
        return False

    def _handle_cue_sheet(self, path):
        cue = cueparser.CueSheet()
        cue.setOutputFormat('%performer% - %title%\n%file%\n%tracks%', '%performer% - %title%')
        with open(path, 'r', encoding='latin1') as f:
            cue.setData(f.read())
        cue.parse()
        tracks = []
        for t in cue.tracks:
            new_track = Track(os.path.join(os.path.dirname(path), cue.file.replace("\\", "\\\\")))
            new_track.artist = cue.title
            new_track.title = t.title
            new_track.index = str(t.number) if t.number else None
            new_track.length = 0 # FIXME: bug in cueparser
            new_track.offset = t.offset if t.offset else 0
            tracks.append(new_track)
        return tracks

    def _handle_file(self, path):
        if not self._is_music_file(path): return None
        track = Track(path)
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
        return track

    def _predicate(self, f):
        if f[0].isdigit():
            try:
                a = re.search('[0-9]+', f).group(0)
                return a.zfill(9)
            except: pass
        return f

    def _handle_dir(self, path):
        cue_files = glob.glob(os.path.join(path, '*.cue'))
        if len(cue_files) > 0:
            tracks = []
            for cue in cue_files:
                tracks.extend(self._handle_cue_sheet(cue))
            return tracks
        return [self._handle_file(os.path.join(path, f))
            for f in sorted(os.listdir(path), key=self._predicate)
                if os.path.isfile(os.path.join(path, f)) and self._is_music_file(f)]

    def _handle_cdda(self):
        device_name = discid.get_default_device()
        disc = discid.read(device_name)
        tracks = []
        for cdda_track in disc.tracks:
            track = Track('cdda://')
            track.title = 'cdda://' # TODO: read tags from FreeDB
            track.index = cdda_track.number
            track.length = cdda_track.seconds
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
            else: return []
        elif os.path.isdir(path):
            return self._handle_dir(path)
        else:
            return []

