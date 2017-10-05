#!/usr/bin/env python3

import urwid
from time import gmtime, strftime
from playerlib.tracks_factory import *

class PlayerController:

    def __init__(self, context):
        self.context = context
        self.tracks_factory = TracksFactory()

    def add_to_playlist(self, path, clear=False):
        tracks = self.tracks_factory.get(path)
        if not tracks or len(tracks) == 0:
            raise RuntimeError('No music files to play!')
        if clear:
            self.context.playlist.clear()
        for f in tracks:
            self.context.playlist.add(f)

    def update_current_state(self, pos):
        if self.context.view.focus_position != 'footer':
            current_track = self.context.playback_controller.current_track
            time_format = '%H:%M:%S' if current_track.length >= 3600 else '%M:%S'
            with self.context.draw_lock:
                self.context.command_panel.set_caption('{} : {} / {}'.format(
                    current_track.title,
                    strftime(time_format, gmtime(pos - current_track.offset)),
                    strftime(time_format, gmtime(current_track.length))))

    def error_handler(self, error):
        self.context.command_panel.error(error)

    def quit(self):
        raise urwid.ExitMainLoop()

