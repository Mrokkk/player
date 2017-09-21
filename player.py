#!/usr/bin/env python3

import os
import time
import urwid

import config
from backends.mplayer import *
from cli.cli import *
from file_browser.file_browser import *
from horizontal_panes import *
from playlist.playlist import *
from track import *
from tracks_factory import *

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
        self.current_track_state = Track.State.STOPPED
        self.tracks_factory = TracksFactory()

    def _update_current_state(self, pos):
        if self.view.focus_position != 'footer':
            time_format = '%H:%M:%S' if self.current_track.track.length >= 3600 else '%M:%S'
            self.cli_panel.set_caption('{} : {} / {}'.format(
                self.current_track.track.title,
                time.strftime(time_format, time.gmtime(pos - self.current_track.track.offset)),
                time.strftime(time_format, time.gmtime(self.current_track.track.length))))

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
        self.backend.play_file(track.track)
        if self.current_track:
            self.current_track.unselect()
        self.current_track = track
        self.current_track.select()
        self.current_track_state = Track.State.PLAYING

    def toggle_pause(self):
        if not self.current_track:
            raise RuntimeError('No track playing!')
        self.backend.toggle_pause()
        if self.current_track_state == Track.State.PAUSED:
            self.current_track_state = Track.State.PLAYING
            self.current_track.select()
        elif self.current_track_state == Track.State.PLAYING:
            self.current_track_state = Track.State.PAUSED
            self.current_track.pause()

    def stop(self):
        if not self.current_track:
            raise RuntimeError('No track playing!')
        self.backend.stop()
        self.current_track.unselect()
        self.current_track = None
        self.current_track_state = Track.State.STOPPED

    def _play_next_track(self, track):
        if not self.current_track:
            raise RuntimeError('No track playing!')
        if not track:
            self.stop()
        else:
            self.play_file(track)

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

