#!/usr/bin/env python3

import os
import queue
import subprocess
import threading
import time
import urwid

class MplayerBackend:

    def __init__(self, event_loop, error_callback, adv_callback):
        self.loop = event_loop
        self.error = error_callback
        self.adv_callback = adv_callback
        self.mplayer = None
        self.current_track = None
        self.should_stop = False

    def _reader(self):
        while True:
            line = self.mplayer.stdout.readline()
            if not line:
                self.mplayer = None
                self.current_track = None
                if not self.should_stop:
                    self.adv_callback()
                self.should_stop = False
                return

    def _send_command(self, command):
        if not self.mplayer: return
        self.mplayer.stdin.write(command.encode())
        self.mplayer.stdin.flush()

    def _run_mplayer(self):
        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue()
        mplayer_args = [
            'mplayer',
            '-ao', 'pulse',
            '-quiet',
            '-slave',
            '-demuxer', 'lavf',
            '-vo', 'null',
            self.current_track.data.path
        ]
        return subprocess.Popen(mplayer_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL)

    def _start_backend(self):
        self.mplayer = self._run_mplayer()
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()

    def play_file(self, item):
        if not item: raise RuntimeError('No track!')
        self.current_track = item
        if not self.mplayer:
            self._start_backend()
        else:
            self._send_command('loadfile "{}"\n'.format(item.data.path))

    def toggle_pause(self):
        self._send_command('pause\n')

    def stop(self):
        if not self.current_track: return
        self.current_track = None
        self.should_stop = True
        self._send_command('stop\n')

    def seek(self, offset):
        self._send_command('seek {} 2 1\n'.format(offset))

    def quit(self):
        if self.mplayer:
            self._send_command('quit\n')
            try:
                self.mplayer.wait(timeout=2)
            except:
                self.mplayer.terminate()

