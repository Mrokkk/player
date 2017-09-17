#!/usr/bin/env python3

import os
import time
import urwid

class Entry(urwid.Button):

    def __init__(self, data):
        self.data = data
        self.name = os.path.basename(data.path)
        super().__init__(self.name)
        if self.data.title:
            self.line = '{}. {} - {} {}'.format(
                self.data.index if self.data.index else '?',
                self.data.artist if self.data.artist else '?',
                self.data.title,
                time.strftime('%H:%M:%S',
                    time.gmtime(int(self.data.length))))
            self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', self.line], -1),
                'file', 'file_focused')
        else:
            self.line = '{} {}'.format(self.name,
                time.strftime('%H:%M:%S',
                    time.gmtime(int(self.data.length))))
            self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', self.line], 0),
                'file', 'file_focused')
        self.prev = None
        self.next = None

    def select(self):
        self._w = urwid.AttrMap(urwid.SelectableIcon(['▸ ', self.line], 0),
            'dir', 'dir_focused')

    def unselect(self):
        self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', self.line], 0),
            'file', 'file_focused')

    def pause(self):
        self._w = urwid.AttrMap(urwid.SelectableIcon(['‖ ', self.line], 0),
            'dir', 'dir_focused')

    def keypress(self, size, key):
        return key

