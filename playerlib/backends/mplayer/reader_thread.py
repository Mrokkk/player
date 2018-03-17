#!/usr/bin/env python3

import csv
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
        try:
            reader = csv.reader(self._mplayer.stdout, delimiter='\r')
        except:
            log_exception(self.logger)
            return
        for row in reader:
            self.logger.debug(row)
            if self._stop_flag.is_set(): return
            if len(row) == 0: continue
            try:
                self._update_time_callback(row[0])
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

