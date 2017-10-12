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
        self.file = None
        self.tracks = []


class CueParser:

    def parse(self, data, use_taglib=False, parent_dir=None):
        if use_taglib: import taglib
        cuesheet = CueSheet()
        current_track = None
        current_file = None
        for raw_line in data:
            line = raw_line.rstrip()
            match = re.match('^REM (.*)$', line)
            if match:
                cuesheet.rem.append(match.group(1))
                continue

            match = re.match('^PERFORMER \"(.*)\"$', line)
            if match:
                cuesheet.performer.append(match.group(1))
                continue

            match = re.match('^TITLE \"(.*)\"$', line)
            if match:
                cuesheet.title.append(match.group(1))
                continue

            match = re.match('^FILE \"(.*)\".*$', line)
            if match:
                current_file = match.group(1)
                if cuesheet.file: cuesheet.file = None
                else: cuesheet.file = current_file
                continue

            match = re.match('^  TRACK ([0-9]+) AUDIO$', line)
            if match:
                if current_track:
                    cuesheet.tracks.append(current_track)
                current_track = CueTrack()
                current_track.index = int(match.group(1))
                current_track.file = current_file
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
                            f = taglib.File(os.path.join(parent_dir, last_track.file.replace("\\", "\\\\")))
                            last_track.length = f.length - last_track.offset
                continue

            match = re.match('^    TITLE \"(.*)\"$', line)
            if match:
                if current_track:
                    current_track.title.append(match.group(1))
                continue

            match = re.match('^    PERFORMER \"(.*)\"$', line)
            if match:
                if current_track:
                    current_track.performer.append(match.group(1))
                continue

        if current_track:
            if use_taglib:
                f = taglib.File(os.path.join(parent_dir, current_track.file.replace("\\", "\\\\")))
                current_track.length = f.length - current_track.offset
            cuesheet.tracks.append(current_track)

        return cuesheet

