#!/usr/bin/env python3

import os
import urwid

import config

class Playlist(urwid.WidgetWrap):

    class Entry(urwid.Button):

        def __init__(self, path):
            self.path = path
            self.name = os.path.basename(path)
            super().__init__(self.name)
            self._w = urwid.AttrMap(urwid.SelectableIcon(['  ', self.name], 0),
                'file', 'file_focused')

        def keypress(self, size, key):
            return key

    def __init__(self):
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
        pass

    def add(self, path):
        self.content.append(self.Entry(path))

