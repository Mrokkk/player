#!/usr/bin/env python3

import os
import urwid
import time

import config

class Playlist(urwid.WidgetWrap):

    class Entry(urwid.Button):

        def __init__(self, data):
            self.data = data
            self.name = os.path.basename(data.path)
            super().__init__(self.name)
            if self.data.title:
                self.line = '{}. {} - {} {}'.format(
                    ', '.join(self.data.index) if self.data.index else '?',
                    ', '.join(self.data.artist) if self.data.artist else '?',
                    ', '.join(self.data.title),
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

        def update_time(self, line):
            self._w = urwid.AttrMap(urwid.SelectableIcon(['▸ ', self.line], 0),
                'dir', 'dir_focused')

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

