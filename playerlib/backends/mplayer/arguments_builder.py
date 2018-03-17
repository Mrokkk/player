#!/usr/bin/env python3

class ArgumentsBuilder:

    def __init__(self, config):
        self._config = config

    def _get_cache(self):
        try: return self._config.cache
        except: return 0

    def _get_demuxer(self, current_track):
        try: return self._config.demuxer[current_track.path.split('.')[-1]]
        except: return 'none'

    def _get_cdrom_device(self):
        try: return self._config.cdrom_device
        except: return '/dev/sr0'

    def build(self, track):
        return [
            self._config.path,
            '-ao', self._config.audio_output,
            '-noquiet',
            '-slave',
            '-cdrom-device', self._get_cdrom_device(),
            '-vo', 'null',
            '-demuxer', self._get_demuxer(track),
            '-cache', str(self._get_cache()),
            '-ss', str(track.offset),
            '-volume', '100',
            track.path
        ]

