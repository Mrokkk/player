#!/usr/bin/env python3

from time import gmtime, strftime

class TracksReaderInterface:

    def _format_seconds_and_get_format_string(self, seconds):
        time_format = '%H:%M:%S' if seconds >= 3600 else '%M:%S'
        return strftime(time_format, gmtime(seconds)), time_format

    def read(self, filename):
        raise NotImplementedError('Not implemented!')

