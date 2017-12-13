#!/usr/bin/env python3

import logging
import re
from time import gmtime, strftime

from playerlib.backends.backend_factory import *
from urwim import clamp, App, rdb, ConstrainedValue

class PlaybackController:

    def __init__(self, context):
        self.context = context
        self.backend = BackendFactory(context.config, self.next, self.update_current_state).create()
        self.current_track = None
        self.volume = 100
        self.logger = logging.getLogger('PlaybackController')
        rdb['volume'] = ConstrainedValue(100, 0, 100)
        rdb.subscribe('volume', self._volume_change)

    def _volume_change(self, new):
        self.backend.set_volume(new)

    def update_current_state(self, pos):
        if pos < 0: return
        app = App()
        if pos - self.current_track.offset >= self.current_track.length and \
                self.current_track.path == self.current_track.playlist_entry.next.track.path:
            self.set_next_track_playing()
        if app.command_panel.selectable() or pos - self.current_track.offset < 0: return
        with app.draw_lock:
            app.command_panel.set_caption('{} : {} / {}'.format(
                self.current_track.title,
                strftime(self.current_track.time_format, gmtime(pos - self.current_track.offset)),
                self.current_track.length_string))

    def play_track(self, track):
        if not track:
            raise RuntimeError('No track!')
        if self.current_track:
            self.current_track.stop()
        self.current_track = track
        self.backend.play_track(self.current_track)
        self.current_track.play()
        self.context.track_info.update(self.current_track)

    def set_next_track_playing(self):
        last_track = self.current_track
        last_track.stop()
        self.current_track = self.current_track.playlist_entry.next.track
        self.current_track.play()
        self.context.track_info.update(self.current_track)

    def pause(self):
        if not self.current_track:
            raise RuntimeError('No track playing!')
        self.backend.toggle_pause()
        self.current_track.toggle_pause()

    def stop(self):
        if not self.current_track:
            raise RuntimeError('No track playing!')
        self.backend.stop()
        self.current_track.stop()
        self.current_track = None
        self.context.track_info.update(None)

    def next(self):
        try:
            self.play_track(self.current_track.playlist_entry.next.track)
        except: self.stop()

    def prev(self):
        try:
            self.play_track(self.current_track.playlist_entry.prev.track)
        except: self.stop()

    def _seek_percentage(self, value):
        match = re.match('^([0-9]+)%$', value)
        if not match: raise RuntimeError('Bad value!')
        self.backend.seek_percentage(int(match.group(1)))

    def _seek_absolute(self, value):
        self.backend.seek(int(value))

    def seek(self, value):
        if not self.current_track:
            raise RuntimeError('No track playing!')
        if '%' in value: self._seek_percentage(value)
        elif value.startswith('-'):
            self.backend.seek_backward(int(value[1:]))
        elif value.startswith('+'):
            self.backend.seek_forward(int(value[1:]))
        else: self._seek_absolute(value)

    def quit(self):
        self.backend.quit()

