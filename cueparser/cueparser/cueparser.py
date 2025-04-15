#!/usr/bin/env python3

import logging
import os
import re

class CueParser:

    class CueTrack:
        def __init__(self, filename, index):
            self.file = filename
            self.index = index
            self.performer = None
            self.title = None
            self.offset = 0
            self.length = 0

        def __repr__(self):
            return str(self.__dict__)


    class CueSheet:
        def __init__(self):
            self.cdtextfile = None
            self.catalog = None
            self.performer = None
            self.rem = []
            self.title = []
            self.tracks = []

        def __repr__(self):
            return str(self.__dict__)


    def __init__(self):
        self.logger = logging.getLogger('CueParser')

    def _update_last_track_in_file(self, parent_dir, track):
        import taglib
        f = taglib.File(os.path.join(parent_dir, track.file))
        track.length = f.length - track.offset

    def _append_regex_match(self, tag_list, regex, line):
        match = re.match(regex, line)
        if match:
            tag_list.append(match.group(1))
            return True

    def _assign_regex_match(self, obj, key, regex, line):
        match = re.match(regex, line)
        if match:
            obj.__dict__[key] = match.group(1).replace("\\", "\\\\")
            return True

    def _parse_file(self, f, use_taglib, parent_dir):
        cuesheet = self.CueSheet()
        current_track = None
        current_file = None
        for raw_line in f:
            line = raw_line.rstrip()

            if self._append_regex_match(cuesheet.rem, r'^REM (.*)$', line): continue
            elif self._assign_regex_match(cuesheet, 'performer', r'^PERFORMER "(.*)"$', line): continue
            elif self._assign_regex_match(cuesheet, 'title', r'^TITLE "(.*)"$', line): continue
            elif self._assign_regex_match(cuesheet, 'cdtextfile', r'^CDTEXTFILE "(.*)"$', line): continue
            elif self._assign_regex_match(cuesheet, 'catalog', r'^CATALOG "(.*)"$', line): continue
            elif current_track:
                if self._assign_regex_match(current_track, 'title', r'^    TITLE "(.*)"$', line): continue
                elif self._assign_regex_match(current_track, 'performer', r'^    PERFORMER "(.*)"$', line): continue

            match = re.match('^FILE "(.*)"', line)
            if match:
                current_file = match.group(1).replace("\\", "\\\\")
                continue

            match = re.match('^  TRACK ([0-9]+) AUDIO$', line)
            if match:
                if current_track:
                    self.logger.debug(current_track)
                    cuesheet.tracks.append(current_track)
                current_track = self.CueTrack(current_file, int(match.group(1)))
                continue

            match = re.match('^    INDEX 01 ([0-9]{2}):([0-9]{2}):([0-9]{2})$', line)
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
            if use_taglib:
                self._update_last_track_in_file(parent_dir, current_track)
            self.logger.debug(current_track)
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
                pass

