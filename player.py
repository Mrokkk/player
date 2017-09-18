#!/usr/bin/env python3

import os
import time
import urwid

from backends.mplayer import *
from cli.cli import *
from file_browser.file_browser import *
from horizontal_panes import *
from playlist.playlist import *
from tracks_factory import *

import config

class PlayerState:
    STOPPED = 0
    PLAYING = 1
    PAUSED = 2

class Player:

    def __init__(self, event_loop, screen):
        self.event_loop = event_loop
        self.screen = screen
        self.playlist = Playlist(self.play_file)
        self.file_browser = FileBrowser(self.add_to_playlist)
        self.cli = Cli(self)
        self.cli_panel = CliPanel(self.cli)
        self.panes = HorizontalPanes([self.file_browser, self.playlist])
        self.view = urwid.Frame(self.panes, footer=self.cli_panel)
        self.main_loop = urwid.MainLoop(
            self.view,
            config.color_palette,
            unhandled_input=self._handle_input,
            event_loop=urwid.AsyncioEventLoop(loop=self.event_loop),
            screen=self.screen)
        self.backend = MplayerBackend(self.event_loop, self._error, self.next, self._update_current_state)
        self.current_track = None
        self.current_track_state = PlayerState.STOPPED
        self.tracks_factory = TracksFactory()

    def _update_current_state(self, pos):
        if self.view.focus_position != 'footer':
            time_format = '%H:%M:%S' if self.current_track.data.length >= 3600 else '%M:%S'
            self.cli_panel.set_caption('{} : {} / {}'.format(
                self.current_track.data.title if self.current_track.data.title else self.current_track.name,
                time.strftime(time_format, time.gmtime(pos - self.current_track.data.offset)),
                time.strftime(time_format, time.gmtime(self.current_track.data.length))))

    def _error(self, error):
        self.cli_panel.set_edit_text('')
        self.cli_panel.set_caption(('error', error))

    def add_to_playlist(self, path, clear=False):
        tracks = self.tracks_factory.get(path)
        if len(tracks) == 0:
            self._error('No music files to play!')
            return
        if clear:
            self.playlist.clear()
        for f in tracks:
            if not f: continue
            self.playlist.add(f)

    def play_file(self, track):
        if not track:
            self._error('No track!')
            return
        if self.current_track:
            if track.data.path == self.current_track.data.path:
                self.current_track.unselect()
                self.current_track = track
                self.current_track.select()
                self.backend.seek(self.current_track.data.offset)
                return
        if self.current_track:
            self.current_track.unselect()
        self.backend.play_file(track)
        self.current_track = track
        self.current_track.select()
        self.current_track_state = PlayerState.PLAYING
        if self.current_track.data.offset != 0:
            self.backend.seek(self.current_track.data.offset)

    def toggle_pause(self):
        if not self.current_track:
            self._error('No track playing!')
            return
        self.backend.toggle_pause()
        if self.current_track_state == PlayerState.PAUSED:
            self.current_track_state = PlayerState.PLAYING
            self.current_track.select()
        elif self.current_track_state == PlayerState.PLAYING:
            self.current_track_state = PlayerState.PAUSED
            self.current_track.pause()

    def stop(self):
        if not self.current_track:
            self._error('No track playing!')
            return
        self.backend.stop()
        self.current_track.unselect()
        self.current_track = None
        self.current_track_state = PlayerState.STOPPED

    def _play_next_track(self, track):
        if not self.current_track:
            self._error('No track playing!')
            return
        self.current_track.unselect()
        try:
            if not track:
                self.stop()
                return
            else:
                self.current_track = None
            self.play_file(track)
        except:
            self.stop()

    def next(self):
        self._play_next_track(self.current_track.next)

    def prev(self):
        self._play_next_track(self.current_track.prev)

    def _handle_input(self, key):
        if key == ':':
            self.view.focus_position = 'footer'
            self.cli_panel.set_caption(':')
            self.cli_panel.set_mode(CliMode.COMMAND)
        elif key == '/':
            self.view.focus_position = 'footer'
            self.cli_panel.set_caption('/')
            self.cli_panel.set_mode(CliMode.SEARCH_FORWARD)
        elif key == 'ctrl w':
            self.panes.switch_focus()
        else:
            if not self.view.focus.unhandled_input(key):
                self.view.focus_position = 'body'

    def quit(self):
        raise urwid.ExitMainLoop()

    def run(self):
        self.main_loop.run()
        self.backend.quit()

