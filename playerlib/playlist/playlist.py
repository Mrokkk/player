#!/usr/bin/env python3

import os
import time
import urwid

from playerlib.helpers.scrollable import *
from .entry import *

class Playlist(urwid.WidgetWrap):

    def __init__(self, play_callback, error_handler):
        self.callback = play_callback
        self.error_handler = error_handler
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
        try_to_scroll(self.listbox, key)
        if key == 'enter':
            try:
                self.callback(self.listbox.focus.track)
            except Exception as e:
                self.error_handler(str(e))

    def _get_track_string(self, track):
        if track.title:
            return '{}. {} - {} {}'.format(
                track.index if track.index else '?',
                track.artist if track.artist else '?',
                track.title,
                time.strftime('%H:%M:%S', time.gmtime(int(track.length))))
        else:
            track.title = os.path.basename(track.path) # FIXME: shouldn't be here
            return '{} {}'.format(track.title, time.strftime('%H:%M:%S', time.gmtime(int(track.length))))

    def add(self, data):
        last = self.content[-1] if len(self.content) > 0 else None
        self.content.append(Entry(data, self._get_track_string(data), prev=last))

    def clear(self):
        self.content[:] = []

