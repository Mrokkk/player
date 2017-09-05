#!/usr/bin/env python3

import os
import urwid

from .entry import *

class Playlist(urwid.WidgetWrap):

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
            return
        try:
            if key[0] == 'mouse press':
                if key[1] == 5.0:
                    self.listbox.focus_position += 1
                elif key[1] == 4.0:
                    self.listbox.focus_position -= 1
        except:
            pass

    def add(self, data):
        last = self.content[-1] if len(self.content) > 0 else None
        new_track = Entry(data)
        new_track.prev = last
        if last:
            last.next = new_track
        self.content.append(new_track)

    def clear(self):
        self.content[:] = []

