#!/usr/bin/env python3

import asyncio
import cueparser
import os
import taglib
import urwid

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
        self.length = 0
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
        self.backend = MplayerBackend(self.event_loop, self._error, self.next)
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
        tracks = []
        for t in cue.tracks:
            new_track = Track(
                os.path.join(os.path.dirname(path), cue.file.replace("\\", "\\\\")),
                offset=t.offset)
            new_track.artist = [cue.title]
            new_track.title = [t.title]
            new_track.index = str(t.number) if t.number else None
            new_track.length = 0 # FIXME: bug in cueparser
            tracks.append(new_track)
        return tracks

    def _handle_file(self, path):
        if not self._is_music_file(path): return []
        track = Track(path)
        tags = taglib.File(path)
        try:
            track.title = tags.tags['TITLE']
        except KeyError: pass
        try:
            track.artist = tags.tags['ARTIST']
        except KeyError: pass
        try:
            track.index = tags.tags['TRACKNUMBER'][0]
        except KeyError: pass
        track.length = tags.length
        return track

    def _get_files(self, path):
        if os.path.isfile(path):
            if path.endswith('.cue'): return self._handle_cue_sheet(path)
            return [self._handle_file(path)]
        elif os.path.isdir(path):
            return [self._handle_file(os.path.join(path, f))
                for f in sorted(os.listdir(path))
                    if os.path.isfile(os.path.join(path, f)) and self._is_music_file(f)]
        else:
            return []

    def add_to_playlist(self, path):
        for f in self._get_files(path):
            self.playlist.add(f)

    def play_file(self, track):
        if not track: raise RuntimeError('No track!')
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
        if not self.current_track: return
        self.backend.toggle_pause()
        if self.current_track_state == PlayerState.PAUSED:
            self.current_track_state = PlayerState.PLAYING
            self.current_track.select()
        elif self.current_track_state == PlayerState.PLAYING:
            self.current_track_state = PlayerState.PAUSED
            self.current_track.pause()

    def stop(self):
        if not self.current_track: return
        self.backend.stop()
        self.current_track.unselect()
        self.current_track = None
        self.current_track_state = PlayerState.STOPPED

    def next(self):
        if not self.current_track: return
        self.current_track.unselect()
        try:
            next_track = self.current_track.next
            self.play_file(next_track)
        except:
            self.stop()

    def prev(self):
        if not self.current_track: return
        self.current_track.unselect()
        try:
            prev_track = self.current_track.prev
            self.play_file(prev_track)
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

    def quit(self):
        raise urwid.ExitMainLoop()

    def run(self):
        self.main_loop.run()
        self.backend.quit()

