#!/usr/bin/env python3

import os
import urwid
import asyncio
import subprocess

import config
from cli import *
from file_browser import *
from horizontal_panes import *
from playlist import *

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
        self.backend = None

    def _start_backend(self, filename):
        backend_args = ['mplayer', '-ao', 'pulse', '-quiet', '-slave', filename]
        self.backend = subprocess.Popen(backend_args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL)
        self.backend_input = self.backend.stdin
        self.backend_output = self.backend.stdout
        if not self.backend: raise RuntimeError('Cannot start backend')

    def _add_to_playlist(self, path):
        self.playlist.add(path)

    def _play_file(self, filename):
        if not self.backend:
            self._start_backend(filename)
            self.backend_output.readline()
        else:
            self.backend_input.write('loadfile "{}"\n'.format(filename).encode())
            self.backend_input.flush()
            self.backend_output.readline()

    def _toggle_pause(self):
        self.backend_input.write('pause\n'.encode())
        self.backend_input.flush()
        self.backend_output.readline()

    def _stop(self):
        self.backend_input.write('stop\n'.encode())
        self.backend_input.flush()
        self.backend_output.readline()

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
            self.backend_input.write('quit\n'.encode())
            self.backend_input.flush()
            self.backend.wait()

