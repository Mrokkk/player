#!/usr/bin/env python3

import logging
import threading
from urwim import log_exception

class ReaderThread(threading.Thread):

    def __init__(self, mplayer, stop_callback, update_time_callback, id):
        self._mplayer = mplayer
        self._stop_callback = stop_callback
        self._update_time_callback = update_time_callback
        self._stop_flag = threading.Event()
        self.logger = logging.getLogger('MplayerReader-{}'.format(id))
        super().__init__(daemon=True)

    def _main_loop(self):
        while True:
            line = self._mplayer.stdout.readline()
            if not line or len(line) == 0: break
            line = line.strip('\r').strip()
            self.logger.debug(line)
            if self._stop_flag.is_set(): return
            try:
                self._update_time_callback(line)
            except Exception as e:
                log_exception(self.logger)

        self._mplayer.wait()
        self._stop_callback()

    def run(self):
        self.logger.debug('Start')
        self._main_loop()
        self.logger.debug('Stop')

    def stop(self):
        self._stop_flag.set()

