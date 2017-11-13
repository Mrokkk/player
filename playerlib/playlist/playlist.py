#!/usr/bin/env python3

import json
import os
import time
import urwid

from playerlib.helpers.scrollable import *
from playerlib.tracks_factory import *
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
        self.tracks_factory = TracksFactory()
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

    def _add_track(self, track):
        last = self.content[-1] if len(self.content) > 0 else None
        self.content.append(Entry(track, self._get_track_string(track), prev=last))

    def add_to_playlist(self, path, clear=False):
        tracks = self.tracks_factory.get(path)
        if not tracks or len(tracks) == 0:
            raise RuntimeError('No music files to play!')
        if clear:
            self.clear()
        for f in tracks:
            self._add_track(f)

    class TrackEncoder(json.JSONEncoder):
        def default(self, o):
            data = o.__dict__.copy()
            del data['state']
            del data['playlist_entry']
            return data

    def save_playlist(self, filename):
        tracks = [t.track for t in self.content]
        with open(filename, 'w') as f:
            json.dump(tracks, f, cls=self.TrackEncoder, indent=1)

    def load_playlist(self, filename):
        # TODO
        pass

    def clear(self):
        self.content[:] = []

