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
        self.current_item = None

    def _parse(self, line):
        splitted = line.strip().split('=')
        key = splitted[0]
        value = splitted[1]
        if key == 'ID_LENGTH':
            self.current_item.update_time(
                time.strftime('%H:%M:%S',
                    time.gmtime(int(round(float(value))))))

    def _reader(self):
        while True:
            line = self.mplayer.stdout.readline()
            if not line:
                self.mplayer = None
                self.adv_callback()
                return
            try:
                self._parse(line.decode('utf-8'))
            except:
                pass

    def _send_command(self, command):
        if not self.mplayer: return
        self.mplayer.stdin.write(command.encode())
        self.mplayer.stdin.flush()

    def _run_mplayer(self):
        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue()
        backend_args = ['mplayer', '-ao', 'pulse', '-quiet', '-slave', '-identify', self.current_item.path]
        return subprocess.Popen(backend_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL)

    def _start_backend(self):
        self.mplayer = self._run_mplayer()
        self.thread = threading.Thread(target=self._reader, daemon=True)
        self.thread.start()

    def play_file(self, item):
        if not item: return
        if self.current_item: self.current_item.unselect()
        self.current_item = item
        self.current_item.select()
        if not self.mplayer:
            self._start_backend()
        else:
            self._send_command('loadfile "{}"\n'.format(item.path))

    def toggle_pause(self):
        self._send_command('pause\n')

    def stop(self):
        self._send_command('stop\n')

    def quit(self):
        if self.mplayer:
            self._send_command('quit\n')
            try:
                self.mplayer.wait(timeout=2)
            except:
                self.mplayer.terminate()

