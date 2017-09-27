#!/usr/bin/env python3

import urwid
from time import gmtime, strftime

import playerlib.config as config
from playerlib.cli.cli import *
from playerlib.file_browser.file_browser import *
from playerlib.horizontal_panes import *
from playerlib.playback_controller import *
from playerlib.playlist.playlist import *
from playerlib.tracks_factory import *

class Player:

    def __init__(self, event_loop, screen):
        self.event_loop = event_loop
        self.screen = screen

        self.playback_controller = PlaybackController(self._update_current_state)
        self.tracks_factory = TracksFactory()

        self.cli = Cli(self)
        self.cli_panel = CliPanel(self.cli)

        self.playlist = Playlist(self.playback_controller.play_file, self._error_handler)
        self.file_browser = FileBrowser(self.add_to_playlist, self._error_handler)
        self.panes = HorizontalPanes([self.file_browser, self.playlist])
        self.view = urwid.Frame(self.panes, footer=self.cli_panel)

        self.main_loop = urwid.MainLoop(
            self.view,
            config.color_palette,
            unhandled_input=self._handle_input,
            event_loop=urwid.AsyncioEventLoop(loop=self.event_loop),
            screen=self.screen)


    def _error_handler(self, error):
        self.cli_panel.set_edit_text('')
        self.cli_panel.set_caption(('error', error))

    def _update_current_state(self, pos):
        if self.view.focus_position != 'footer':
            current_track = self.playback_controller.current_track
            time_format = '%H:%M:%S' if current_track.length >= 3600 else '%M:%S'
            self.cli_panel.set_caption('{} : {} / {}'.format(
                current_track.title,
                strftime(time_format, gmtime(pos - current_track.offset)),
                strftime(time_format, gmtime(current_track.length))))

    def add_to_playlist(self, path, clear=False):
        tracks = self.tracks_factory.get(path)
        if len(tracks) == 0:
            raise RuntimeError('No music files to play!')
        if clear:
            self.playlist.clear()
        for f in tracks:
            self.playlist.add(f)

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
            if key == ' ':
                self.playback_controller.toggle_pause()
                return
            if not self.view.focus.unhandled_input(key):
                self.view.focus_position = 'body'

    def quit(self):
        raise urwid.ExitMainLoop()

    def run(self):
        try:
            self.main_loop.run()
        except Exception as e:
            print(str(e))
        finally:
            self.playback_controller.quit()

