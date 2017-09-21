#!/usr/bin/env python3

import os
import time
import urwid

class Entry(urwid.Button):

    def __init__(self, track, line, prev=None):
        self.track = track
        super().__init__('')
        self.line = line
        self.unselect()
        self.prev = prev
        self.next = None
        if prev:
            prev.next = self

    def select(self):
        self._w = urwid.AttrMap(urwid.SelectableIcon(['▸ ', self.line]), 'dir', 'dir_focused')

    def unselect(self):
        self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', self.line]), 'file', 'file_focused')

    def pause(self):
        self._w = urwid.AttrMap(urwid.SelectableIcon(['‖ ', self.line]), 'dir', 'dir_focused')

    def keypress(self, size, key):
        return key

