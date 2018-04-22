#!/usr/bin/env python3

from time import gmtime, strftime
from playerlib.track.track import *
from .tracks_reader_interface import *

class CdaudioReader(TracksReaderInterface):

    def __init__(self):
        pass

    def _format_seconds_and_get_format_string(self, seconds):
        time_format = '%H:%M:%S' if seconds >= 3600 else '%M:%S'
        return strftime(time_format, gmtime(seconds)), time_format

    def read(self, path):
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

