#!/usr/bin/env python3

import os
import re

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


class CueParser:

    def _update_last_track_in_file(self, parent_dir, track):
        import taglib
        f = taglib.File(os.path.join(parent_dir, track.file))
        track.length = f.length - track.offset

    def _add_regex_match_to_list(self, tag_list, regex, line):
        match = re.match(regex, line)
        if match:
            tag_list.append(match.group(1))
            return True

    def _parse_file(self, f, use_taglib, parent_dir):
        cuesheet = CueSheet()
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
                current_track = CueTrack()
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
        try:
            with open(path, 'r', encoding='latin1') as f:
                return self._parse_file(f, use_taglib, parent_dir)
        except: pass
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return self._parse_file(f, use_taglib, parent_dir)
        except: pass

