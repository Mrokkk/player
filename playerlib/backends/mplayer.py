#!/usr/bin/env python3

import csv
import logging
import os
import queue
import re
import subprocess
import sys
import threading
import traceback

class MplayerBackend:

    def __init__(self, adv_callback, set_time_callback, path):
        self.adv_callback = adv_callback
        self.set_time_callback = set_time_callback
        self.mplayer_path = path
        self.mplayer = None
        self.current_track = None
        self.should_stop = False
        self.stop_updating_time = False
        self.logger = logging.getLogger('MplayerBackend')

    def _update_time_pos(self, line):
        if self.stop_updating_time: return
        match = re.match('^A:[ \t]{0,}([0-9]+).*$', line)
        if not match: return
        self.set_time_callback(int(match.group(1)))

    def _reader(self):
        while True:
            reader = csv.reader(self.mplayer.stdout, delimiter='\r')
            for row in reader:
                if len(row) == 0: continue
                try: self._update_time_pos(row[0])
                except Exception as e:
                    tb = traceback.format_exc().split('\n')
                    for trace in tb:
                        self.logger.warning(trace)
            line = self.mplayer.stdout.readline()
            if line: continue
            self.logger.info('MPlayer exitted')
            self.mplayer = None
            self.current_track = None
            if not self.should_stop:
                try:
                    self.logger.info('Starting next track')
                    self.adv_callback()
                except: pass
            self.should_stop = False

    def _send_command(self, command):
        if not self.mplayer: return
        self.logger.info('Sending command: {}'.format(command.strip()))
        self.mplayer.stdin.write(command)
        self.mplayer.stdin.flush()

    def _build_mplayer_args(self):
        cache = 8192
        if self.current_track.path == 'cdda://':
            demuxer = 'rawaudio'
        elif self.current_track.path.endswith('.flac'):
            demuxer = 'lavf'
        elif self.current_track.path.endswith('.ape'):
            demuxer = 'lavf'
        elif self.current_track.path.endswith('.mp3'):
            demuxer = 'audio'
        else:
            demuxer = 'none'
        return [
            self.mplayer_path,
            '-ao', 'pulse',
            '-noquiet',
            '-slave',
            '-cdrom-device', '/dev/cdrom',
            '-vo', 'null',
            '-demuxer', demuxer,
            '-cache', str(cache),
            '-ss', str(self.current_track.offset),
            self.current_track.path
        ]

    def _start_backend(self):
        mplayer_args = self._build_mplayer_args()
        self.logger.info('Starting mplayer with args: {}'.format(mplayer_args))
        self.mplayer = subprocess.Popen(mplayer_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            encoding='utf-8',
            preexec_fn=lambda: os.setpgrp())
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()

    def _loadfile(self, path):
        self._send_command('loadfile "{}"\n'.format(path))

    def play_track(self, track):
        if not track: raise RuntimeError('No track!')
        self.stop_updating_time = True
        last_track = self.current_track
        self.current_track = track
        if not self.mplayer:
            self._start_backend()
        else:
            if self.current_track.path != last_track.path:
                self._loadfile(track.path)
        if self.current_track == last_track:
            self.seek(self.current_track.offset)
        else:
            if (last_track and self.current_track.path == last_track.path) or \
                    (not last_track and self.current_track.offset > 0):
                self.seek(self.current_track.offset)
        self.stop_updating_time = False

    def toggle_pause(self):
        if not self.current_track: return
        self._send_command('pause\n')

    def stop(self):
        if not self.current_track: return
        self.stop_updating_time = True
        self.current_track = None
        self.should_stop = True
        self._send_command('stop\n')

    def seek(self, offset):
        self._send_command('seek {} 2 1\n'.format(offset))

    def seek_percentage(self, percent):
        self._send_command('seek {} 1\n'.format(percent))

    def seek_forward(self, time):
        self._send_command('seek +{} 0\n'.format(time))

    def seek_backward(self, time):
        self._send_command('seek -{} 0\n'.format(time))

    def quit(self):
        if self.mplayer:
            self.should_stop = True
            self._send_command('quit\n')
            try:
                self.mplayer.wait(timeout=2)
            except:
                self.mplayer.terminate()

