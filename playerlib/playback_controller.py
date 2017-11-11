#!/usr/bin/env python3

import logging
import re
from time import gmtime, strftime

from playerlib.backends.backend_factory import *

class PlaybackController:

    def __init__(self, context):
        self.context = context
        self.backend = BackendFactory().create(context.config, self.next, self.update_current_state)
        self.current_track = None
        self.logger = logging.getLogger('PlaybackController')

    def update_current_state(self, pos):
        if pos < 0: return
        if pos - self.current_track.offset >= self.current_track.length and \
                self.current_track.path == self.current_track.playlist_entry.next.track.path:
            self.set_next_track_playing()
        if self.context.view.focus_position != 'footer':
            if pos - self.current_track.offset < 0: return
            time_format = '%H:%M:%S' if self.current_track.length >= 3600 else '%M:%S'
            with self.context.draw_lock:
                self.context.command_panel.set_caption('{} : {} / {}'.format(
                    self.current_track.title,
                    strftime(time_format, gmtime(pos - self.current_track.offset)),
                    strftime(time_format, gmtime(self.current_track.length))))

    def play_track(self, track):
        if not track:
            raise RuntimeError('No track!')
        if self.current_track:
            self.current_track.stop()
        self.current_track = track
        self.backend.play_track(self.current_track)
        self.current_track.play()

    def set_next_track_playing(self):
        last_track = self.current_track
        last_track.stop()
        self.current_track = self.current_track.playlist_entry.next.track
        self.current_track.play()

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

    def _seek_offset(self, value):
        if value.startswith('-'):
            self.backend.seek_backward(int(value[1:]))
        elif value.startswith('+'):
            self.backend.seek_forward(int(value[1:]))

    def _seek_absolute(self, value):
        self.backend.seek(int(value))

    def seek(self, value):
        if not self.current_track:
            raise RuntimeError('No track playing!')
        if '%' in value: self._seek_percentage(value)
        elif '+' in value or '-' in value: self._seek_offset(value)
        else: self._seek_absolute(value)

    def quit(self):
        self.backend.quit()

