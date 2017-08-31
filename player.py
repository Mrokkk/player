#!/usr/bin/env python3

import asyncio
import os
import queue
import select
import subprocess
import threading
import time
import urwid

import config
from cli import *
from file_browser import *
from horizontal_panes import *
from playlist import *

class MplayerBackend:

    def __init__(self, event_loop, error_callback):
        self.loop = event_loop
        self.error = error_callback
        self.mplayer = None
        self.current_item = None

    def _error(self):
        self.error('Failed to play')
        self.mplayer = None
        if self.current_item: self.current_item.unselect()
        return

    def _controller(self):
        os.read(self.mplayer.stdout.fileno(), 4096)
        time.sleep(1)
        if self.mplayer.poll() != None:
            self._error()
            return
        os.read(self.mplayer.stdout.fileno(), 4096)
        self.thread2.start()
        while True:
            data = self.input_queue.get()
            self.mplayer.stdin.write(data.encode())
            self.mplayer.stdin.flush()
            time.sleep(1)
            if self.mplayer.poll() != None:
                self._error()
                return
            os.read(self.mplayer.stdout.fileno(), 4096)

    def _run_mplayer(self):
        self.output_queue = queue.Queue()
        self.input_queue = queue.Queue()
        backend_args = ['mplayer', '-ao', 'pulse', '-quiet', '-slave', self.current_item.path]
        return subprocess.Popen(backend_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL)

    def _time_check(self):
        self.mplayer.stdin.write('get_time_length\n'.encode())
        self.mplayer.stdin.flush()
        length = self.mplayer.stdout.readline().decode('ascii').strip().split('=')[1]
        while True:
            self.mplayer.stdin.write('get_time_pos\n'.encode())
            self.mplayer.stdin.flush()
            data = self.mplayer.stdout.readline().decode('ascii').strip().split('=')[1]
            self.current_item.update_time('{}/{}'.format(
                time.strftime('%H:%M:%S', time.gmtime(int(round(float(data))))),
                time.strftime('%H:%M:%S', time.gmtime(int(round(float(length)))))))
            time.sleep(0.2)

    def _start_backend(self):
        self.mplayer = self._run_mplayer()
        self.thread = threading.Thread(target=self._controller, daemon=True)
        self.thread2 = threading.Thread(target=self._time_check, daemon=True)
        self.thread.start()

    def play_file(self, item):
        if self.current_item: self.current_item.unselect()
        self.current_item = item
        self.current_item.select()
        if not self.mplayer:
            self._start_backend()
        else:
            self.input_queue.put('loadfile "{}"\n'.format(item.path))

    def quit(self):
        if self.mplayer:
            self.mplayer.stdin.write('quit\n'.encode())
            self.mplayer.stdin.flush()
            try:
                self.mplayer.wait(timeout=1)
            except:
                self.mplayer.terminate()


class Player:

    def __init__(self):
        self.playlist = Playlist(self._play_file)
        self.file_browser = FileBrowser(self._add_to_playlist)
        self.cli = Cli()
        self.cli_panel = CliPanel(self.cli)
        self.panes = HorizontalPanes([self.file_browser, self.playlist])
        self.view = urwid.Frame(self.panes, footer=self.cli_panel)
        self.screen = self._create_screen()
        self.event_loop = asyncio.get_event_loop()
        self.main_loop = urwid.MainLoop(
            self.view,
            config.color_palette,
            unhandled_input=self._handle_input,
            event_loop=urwid.AsyncioEventLoop(loop=self.event_loop),
            screen=self.screen)
        self.backend = MplayerBackend(self.event_loop, self._error)

    def _error(self, error):
        self.cli_panel.set_edit_text('')
        self.cli_panel.set_caption(('error', error))

    def _add_to_playlist(self, path):
        self.playlist.add(path)

    def _play_file(self, item):
        self.backend.play_file(item)

    def _toggle_pause(self):
        pass

    def _stop(self):
        pass

    def _handle_input(self, key):
        if key == ':':
            self.view.focus_position = 'footer'
            self.cli_panel.set_caption(':')
        elif key == 'ctrl w':
            self.panes.switch_focus()
        else:
            path = self.view.focus.unhandled_input(key)
            self.view.focus_position = 'body'

    def _create_screen(self):
        screen = urwid.raw_display.Screen()
        try:
            screen.set_terminal_properties(256)
        except:
            pass
        return screen

    def run(self):
        self.main_loop.run()
        if self.backend:
            self.backend.quit()

