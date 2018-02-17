#!/usr/bin/env python3

import urwim

class Entry(urwim.ListBoxEntry):

    def __init__(self, track, line, prev=None):
        self.track = track
        self.track.playlist_entry = self
        super().__init__('')
        self.line = line
        self.set_stopped()
        self.prev = prev
        self.next = None
        if prev:
            prev.next = self

    def set_playing(self):
        self.update(['▸ ', self.line], 'dir', 'dir_focused')

    def set_stopped(self):
        self.update(['  ', self.line], 'file', 'file_focused')

    def set_paused(self):
        self.update(['‖ ', self.line], 'dir', 'dir_focused')

    @property
    def text(self):
        return self.line

