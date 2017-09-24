#!/usr/bin/env python3

from time import gmtime, strftime
from playerlib.backends.mplayer import *

class PlaybackController:

    def __init__(self):
        self.backend = MplayerBackend(self.next, None)
        self.current_track = None

    def _update_current_state(self, pos):
        if self.view.focus_position != 'footer':
            time_format = '%H:%M:%S' if self.current_track.length >= 3600 else '%M:%S'
            self.cli_panel.set_caption('{} : {} / {}'.format(
                self.current_track.title,
                strftime(time_format, gmtime(pos - self.current_track.offset)),
                strftime(time_format, gmtime(self.current_track.length))))

    def play_file(self, track):
        if not track:
            raise RuntimeError('No track!')
        if self.current_track:
            self.current_track.stop()
        self.current_track = track.track
        self.backend.play_file(self.current_track)
        self.current_track.play()

    def toggle_pause(self):
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
        self._play_next_track(self.current_track.playlist_entry.next)

    def prev(self):
        self._play_next_track(self.current_track.playlist_entry.prev)

    def quit(self):
        self.backend.quit()

