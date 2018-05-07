#!/usr/bin/env python3

from urwim import rdb

class ArgumentsBuilder:

    def __init__(self, config):
        self._config = config

    def _get_audio_output(self):
        try: self._config.audio_output
        except: return 'pulse'

    def _get_cache(self):
        try: return self._config.cache
        except: return 0

    def _get_demuxer(self, current_track):
        try: return self._config.demuxer[current_track.path.split('.')[-1]]
        except: return None

    def _get_cdrom_device(self):
        try: return self._config.cdrom_device
        except: return '/dev/sr0'

    def _get_volume(self):
        try: return rdb['volume']
        except: return 100

    def build(self, track):
        args = [
            self._config.path,
            '-ao', self._get_audio_output(),
            '-noquiet',
            '-slave',
            '-novideo',
            '-cdrom-device', self._get_cdrom_device(),
            '-vo', 'null',
            '-cache', str(self._get_cache()),
            '-ss', str(track.offset),
            '-volume', str(self._get_volume()),
        ]
        demuxer = self._get_demuxer(track)
        if demuxer:
            args.extend(['-demuxer', demuxer])
        args.append(track.path)
        return args

