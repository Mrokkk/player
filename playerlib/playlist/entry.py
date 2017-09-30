#!/usr/bin/env python3

import urwid

class Entry(urwid.Button):

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
        self._w = urwid.AttrMap(urwid.SelectableIcon(['▸ ', self.line], 0), 'dir', 'dir_focused')

    def set_stopped(self):
        self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', self.line], 0), 'file', 'file_focused')

    def set_paused(self):
        self._w = urwid.AttrMap(urwid.SelectableIcon(['‖ ', self.line], 0), 'dir', 'dir_focused')

    def keypress(self, size, key):
        return key

