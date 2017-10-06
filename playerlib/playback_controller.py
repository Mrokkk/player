#!/usr/bin/env python3

import re

class PlaybackController:

    def __init__(self, backend_factory):
        self.backend_factory = backend_factory
        self.backend = None
        self.current_track = None

    def play_file(self, track):
        if not track:
            raise RuntimeError('No track!')
        if not self.backend:
            self.backend = self.backend_factory.create()
        if self.current_track:
            self.current_track.stop()
        self.current_track = track
        self.backend.play_file(self.current_track)
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

    def _play_next_track(self, track):
        if not self.current_track:
            raise RuntimeError('No track playing!')
        if not track:
            self.stop()
        else:
            self.play_file(track)

    def next(self):
        self._play_next_track(self.current_track.playlist_entry.next.track)

    def prev(self):
        self._play_next_track(self.current_track.playlist_entry.prev.track)

    def _seek_percentage(self, value):
        match = re.match('([0-9]+)%', value)
        if not match: raise RuntimeError('Bad value!')
        self.backend.seek_percentage(int(match.group(1)))

    def _seek_offset(self, value):
        if value.startswith('-'):
            self.backend.seek_backward(int(value[1:]))
        elif value.startswith('+'):
            self.backend.seek_forward(int(value[1:]))
        else:
            raise RuntimeError('Bad value!')

    def _seek_absolute(self, value):
        self.backend.seek(int(value))

    def seek(self, value):
        if not self.current_track:
            raise RuntimeError('No track playing!')
        if '%' in value: self._seek_percentage(value)
        elif '+' in value or '-' in value: self._seek_offset(value)
        else: self._seek_absolute(value)

    def quit(self):
        if self.backend:
            self.backend.quit()

