#!/usr/bin/env python3

import asyncio
import os
import urwid
import cueparser

from cli import *
from file_browser.file_browser import *
from horizontal_panes import *
from playlist import *

from backends.mplayer import *

import config

class PlayerState:
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2


class Track:

    def __init__(self, file_path, offset=0):
        self.path = file_path
        self.offset = offset # For CUE sheets
        self.length = None
        self.index = 0
        self.title = None
        self.artist = None
        self.performer = None
        self.state = None


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
        self.current_track = None
        self.current_track_state = PlayerState.STOPPED

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
            self._error(e.__str__())
        return [Track(os.path.dirname(path) + '/' + cue.file.replace("\\", "\\\\"), offset=t.offset)
            for t in cue.tracks]

    def _get_files(self, path):
        if os.path.isfile(path):
            if path.endswith('.cue'): return self._handle_cue_sheet(path)
            return [Track(path)] if self._is_music_file(path) else []
        elif os.path.isdir(path):
            return [Track(os.path.join(path, f))
                for f in sorted(os.listdir(path))
                    if os.path.isfile(os.path.join(path, f)) and self._is_music_file(f)]
        else:
            return []

    def add_to_playlist(self, path):
        for f in self._get_files(path):
            self.playlist.add(f)

    def play_file(self, item):
        track = item.data
        if not track: raise RuntimeError('No track!')
        if track == self.current_track:
            self.backend.seek(self.current_track.offset)
            return
        self.backend.play_file(item)
        self.current_track = track
        self.current_track_state = PlayerState.PLAYING
        if self.current_track.offset != 0:
            self.backend.seek(self.current_track.offset)

    def toggle_pause(self):
        if not self.current_track: return
        self.backend.toggle_pause()
        self.current_track_state = PlayerState.PLAYING if self.current_track_state == PlayerState.STOPPED else PlayerState.STOPPED

    def stop(self):
        if not self.current_track: return
        self.backend.stop()
        self.current_track = None
        self.current_track_state = PlayerState.STOPPED

    def advance(self):
        if not self.current_track: return
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

