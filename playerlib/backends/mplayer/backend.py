#!/usr/bin/env python3

import logging
import os
import re
import subprocess

from .arguments_builder import *
from .reader_thread import *
from ..backend_interface import *

class Backend(BackendInterface):

    def __init__(self, adv_callback, set_time_callback, config):
        self.config = config
        self.adv_callback = adv_callback
        self.set_time_callback = set_time_callback
        self.mplayer = None
        self.current_track = None
        self.should_stop = False
        self._thread = None
        self._thread_id_counter = 0
        self._arguments_builder = ArgumentsBuilder(config)
        self.logger = logging.getLogger('MplayerBackend')
        super().__init__()

    def _update_time_pos(self, line):
        match = re.match('^A:[ \t]{0,}([0-9]+)', line)
        if not match: return
        if not self.current_track:
            self.logger.warning('Trying to update time for stopped track!')
            return
        self.set_time_callback(int(match.group(1)))

    def _mplayer_stopped(self):
        self.logger.info('MPlayer exitted')
        self.mplayer = None
        self._thread = None
        if not self.should_stop:
            try:
                self.logger.info('Starting next track')
                self.adv_callback()
            except: pass
        self.should_stop = False

    def _send_command(self, command):
        if not self.mplayer:
            self.logger.warning('No mplayer running')
            return
        self.logger.info('Sending command: {}'.format(command.strip()))
        try:
            self.mplayer.stdin.write(command)
            self.mplayer.stdin.flush()
        except IOError:
            self.mplayer.terminate()
            self.mplayer = None

    def _start_thread(self):
        self._thread = ReaderThread(self.mplayer, self._mplayer_stopped,
            self._update_time_pos, self._thread_id_counter)
        self._thread.start()
        self._thread_id_counter += 1

    def _start_backend(self):
        mplayer_args = self._arguments_builder.build(self.current_track)
        self.logger.info('Starting mplayer with args: {}'.format(' '.join(mplayer_args)))
        self.mplayer = subprocess.Popen(mplayer_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            encoding='utf-8',
            errors='ignore',
            preexec_fn=lambda: os.setpgrp())

    def _loadfile(self, path):
        self._send_command('loadfile "{}"\n'.format(path))

    def play_track(self, track):
        if not track: raise RuntimeError('No track!')
        if self._thread: self._thread.stop()
        last_track = self.current_track
        self.current_track = track
        if not self.mplayer or not last_track:
            self._start_backend()
        else:
            if self.current_track.path != last_track.path:
                self._loadfile(track.path)
                if self.current_track.offset:
                    self.seek(self.current_track.offset)
        if self.current_track == last_track:
            self.seek(self.current_track.offset)
        else:
            if last_track and self.current_track.path == last_track.path:
                self.seek(self.current_track.offset)
        self._start_thread()
        self.should_stop = False

    def toggle_pause(self):
        if not self.current_track: return
        self._send_command('pause\n')

    def stop(self):
        if not self.current_track: return
        self.current_track = None
        self.should_stop = True
        self._send_command('stop\n')

    def seek(self, offset):
        if not self.current_track: return
        self._send_command('seek {} 2 1\n'.format(offset))

    def seek_percentage(self, percent):
        if not self.current_track: return
        self._send_command('seek {} 1\n'.format(percent))

    def seek_forward(self, time):
        if not self.current_track: return
        self._send_command('seek +{} 0\n'.format(time))

    def seek_backward(self, time):
        if not self.current_track: return
        self._send_command('seek -{} 0\n'.format(time))

    def set_volume(self, volume):
        self._send_command('volume {} 1\n'.format(volume))

    def quit(self):
        if self.mplayer:
            self.should_stop = True
            self._send_command('quit\n')
            try:
                self.mplayer.wait(timeout=2)
            except:
                self.mplayer.terminate()

