#!/usr/bin/env python3

import logging
import os
import re

from time import gmtime, strftime
from playerlib.track.track import *
from .tracks_reader_interface import *

class CueParser:

    class CueTrack:
        def __init__(self):
            self.file = None
            self.performer = []
            self.title = []
            self.index = None
            self.offset = 0
            self.length = 0


    class CueSheet:
        def __init__(self):
            self.rem = []
            self.performer = []
            self.artist = []
            self.title = []
            self.tracks = []

    def __init__(self):
        self.logger = logging.getLogger('CueParser')

    def _update_last_track_in_file(self, parent_dir, track):
        try:
            import taglib
        except:
            self.logger.warning('Cannot import taglib')
            return
        f = taglib.File(os.path.join(parent_dir, track.file))
        track.length = f.length - track.offset

    def _add_regex_match_to_list(self, tag_list, regex, line):
        match = re.match(regex, line)
        if match:
            tag_list.append(match.group(1))
            return True

    def _parse_file(self, f, use_taglib, parent_dir):
        cuesheet = self.CueSheet()
        current_track = None
        current_file = None
        for raw_line in f:
            line = raw_line.rstrip()

            if self._add_regex_match_to_list(cuesheet.rem, '^REM (.*)$', line): continue
            elif self._add_regex_match_to_list(cuesheet.performer, '^PERFORMER \"(.*)\"$', line): continue
            elif self._add_regex_match_to_list(cuesheet.title, '^TITLE \"(.*)\"$', line): continue

            match = re.match('^FILE \"(.*)\".*$', line)
            if match:
                current_file = match.group(1).replace("\\", "\\\\")
                continue

            match = re.match('^  TRACK (\d+) AUDIO$', line)
            if match:
                if current_track:
                    cuesheet.tracks.append(current_track)
                current_track = self.CueTrack()
                current_track.index = int(match.group(1))
                current_track.file = current_file
                continue

            match = re.match('^    INDEX 01 (\d{2}):(\d{2}):(\d{2})$', line)
            if match:
                if current_track:
                    current_track.offset = int(match.group(1)) * 60 + int(match.group(2))
                    if len(cuesheet.tracks) > 0:
                        last_track = cuesheet.tracks[-1]
                        if last_track.file == current_track.file:
                            last_track.length = current_track.offset - last_track.offset
                        elif use_taglib:
                            self._update_last_track_in_file(parent_dir, last_track)
                continue

            if current_track:
                if self._add_regex_match_to_list(current_track.title, '^    TITLE \"(.*)\"$', line): continue
                elif self._add_regex_match_to_list(current_track.performer, '^    PERFORMER \"(.*)\"$', line): continue

        if current_track:
            if use_taglib:
                self._update_last_track_in_file(parent_dir, current_track)
            cuesheet.tracks.append(current_track)

        return cuesheet


    def parse(self, path, use_taglib=False):
        parent_dir = os.path.dirname(path)
        encodings = ['utf-8', 'windows-1250', 'latin2']
        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    return self._parse_file(f, use_taglib, parent_dir)
            except Exception as e:
                self.logger.warning('Cannot open {} using encoding {}: {}'.format(path, encoding, str(e)))


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

