#!/usr/bin/env python3

import asyncio
import os
import urwid
import cueparser

import traceback

from cli import *
from file_browser.file_browser import *
from horizontal_panes import *
from playlist import *

from backends.mplayer import *

import config

class Player:

    extensions = [
        '.mp3', '.flac', '.m4a', '.wma', '.ogg', '.ape', '.alac', '.mpc', '.wav', '.wv'
    ]

    def __init__(self):
        self.playlist = Playlist(self.play_file)
        self.file_browser = FileBrowser(self.add_to_playlist)
        self.cli = Cli(self)
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
        self.backend = MplayerBackend(self.event_loop, self._error, self.advance)

    def _error(self, error):
        self.cli_panel.set_edit_text('')
        self.cli_panel.set_caption(('error', error))

    def _is_music_file(self, path):
        for e in self.extensions:
            if path.endswith(e): return True
        return False

    def _handle_cue_sheet(self, path):
        cue = cueparser.CueSheet()
        cue.setOutputFormat('%performer% - %title%\n%file%\n%tracks%', '%performer% - %title%')
        try:
            with open(path, 'r', encoding='latin1') as f:
                data = f.read()
                cue.setData(data)
            cue.parse()
        except Exception as e:
            print(traceback.format_exc())
        return [t.title for t in cue.tracks]

    def _get_files(self, path):
        if os.path.isfile(path):
            if path.endswith('.cue'): return self._handle_cue_sheet(path)
            return [path] if self._is_music_file(path) else []
        elif os.path.isdir(path):
            return [os.path.join(path, f) for f in sorted(os.listdir(path)) if os.path.isfile(os.path.join(path, f)) and self._is_music_file(f)]
        else:
            return []

    def add_to_playlist(self, path):
        for f in self._get_files(path):
            self.playlist.add(f)

    def play_file(self, item):
        self.backend.play_file(item)

    def toggle_pause(self):
        self.backend.toggle_pause()

    def stop(self):
        self.backend.stop()

    def advance(self):
        current = self.playlist.get_current()
        current.unselect()
        try:
            next_item = self.playlist.get_next()
            next_item.select()
            self.play_file(next_item)
        except:
            self.stop()

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
        self.backend.quit()

