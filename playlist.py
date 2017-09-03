#!/usr/bin/env python3

import os
import urwid

import config

class Playlist(urwid.WidgetWrap):

    class Entry(urwid.Button):

        def __init__(self, data):
            self.data = data
            self.name = os.path.basename(data.path)
            super().__init__(self.name)
            self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', self.name], 0),
                'file', 'file_focused')
            self.prev = None
            self.next = None

        def update_time(self, line):
            self._w = urwid.AttrMap(urwid.SelectableIcon(['▸ ', self.name + ' : ' + line], 0),
                'dir', 'dir_focused')

        def select(self):
            self._w = urwid.AttrMap(urwid.SelectableIcon(['▸ ', self.name], 0),
                'dir', 'dir_focused')

        def unselect(self):
            self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', self.name], 0),
                'file', 'file_focused')

        def pause(self):
            self._w = urwid.AttrMap(urwid.SelectableIcon(['‖ ', self.name], 0),
                'dir', 'dir_focused')

        def keypress(self, size, key):
            return key

    def __init__(self, play_callback):
        self.callback = play_callback
        self.list = []
        self.content = urwid.SimpleListWalker([])
        self.listbox = urwid.ListBox(self.content)
        self.header = urwid.AttrWrap(urwid.Text('Unnamed playlist'), 'head')
        self.footer = urwid.AttrWrap(urwid.Text('Playlist'), 'foot')
        super().__init__(urwid.Frame(
            self.listbox,
            header=self.header,
            footer=self.footer))

    def unhandled_input(self, key):
        if key == 'enter':
            self.callback(self.listbox.focus)

    def add(self, data):
        last = self.content[-1] if len(self.content) > 0 else None
        new_track = self.Entry(data)
        new_track.prev = last
        if last:
            last.next = new_track
        self.content.append(new_track)

