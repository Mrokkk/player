#!/usr/bin/env python3

from playerlib.track.track import *
from .tracks_reader_interface import *

class CdaudioReader(TracksReaderInterface):

    def read(self, path):
        if path != 'cdda://': return None
        try:
            import discid
        except:
            raise RuntimeError('Cannot import discid. Is it installed?')
        device_name = discid.get_default_device()
        disc = discid.read(device_name)
        tracks = []
        for cdda_track in disc.tracks:
            track = Track()
            track.path = path
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

