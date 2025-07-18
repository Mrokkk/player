#!/usr/bin/env python3

import json
import logging
import os
import time
import urwim
from typing import Any, Callable

from playerlib.track.track import *
from playerlib.track.tracks_reader import *
from .entry import *

class Playlist(urwim.ViewWidget):

    play_callback: Callable[[Track], None]
    content:       urwim.SimpleListWalker
    listbox:       urwim.ListWidget
    header:        urwim.Header
    tracks_reader: TracksReader
    logger:        logging.Logger

    def __init__(self, play_callback: Callable[[Track], None]):
        self.play_callback = play_callback
        self.content = urwim.SimpleListWalker([])

        self.listbox = urwim.ListWidget(
            self.content,
            on_delete=lambda x: self._relink_playlist(),
            on_paste=lambda x: self._on_paste(x))

        self.header = urwim.Header('Unnamed playlist')
        self.tracks_reader = TracksReader()
        self.logger = logging.getLogger('Playlist')

        callbacks = {
            'enter': lambda: self.play_callback(self.listbox.focus.track)
        }

        super().__init__(
            self.listbox,
            'Playlist',
            callbacks=callbacks,
            header=self.header)

    def _get_track_string(self, track: Track) -> str:
        if track.title:
            return '{}. {} - {} {}'.format(
                track.index if track.index else '?',
                track.artist if track.artist else '?',
                track.title,
                time.strftime('%H:%M:%S', time.gmtime(int(track.length))))
        else:
            return '{} {}'.format(os.path.basename(track.path), time.strftime('%H:%M:%S', time.gmtime(int(track.length))))

    def _add_track(self, track: Track) -> None:
        last = self.content[-1] if len(self.content) > 0 else None
        self.content.append(Entry(track, self._get_track_string(track), prev=last))

    def add_to_playlist(self, path: str, clear_and_play: bool = False) -> None:
        tracks = self.tracks_reader.read(path)
        if not tracks or len(tracks) == 0:
            raise RuntimeError('No music files to play!')
        if clear_and_play:
            self.clear()
        for f in tracks:
            self._add_track(f)
        if clear_and_play:
            try:
                self.listbox.focus_position = 0
                self.play_callback(self.listbox.focus.track)
            except: pass

    def save_playlist(self, filename: str) -> None:
        tracks = [t.track.to_dict() for t in self.content]
        with open(filename, 'w') as f:
            json.dump(tracks, f, indent=1)
        self.header.text = filename

    def load_playlist(self, filename: str) -> None:
        with open(filename, 'r') as f:
            raw_tracks = json.load(f)
        for t in raw_tracks:
            self._add_track(Track(t))
        self.header.text = filename

    def clear(self) -> None:
        self.content[:] = []

    def _relink_playlist(self) -> None:
        prev = None
        for e in self.content:
            e.prev = prev
            if prev: prev.next = e
            prev = e
        self.content[-1].next = None

    def _on_paste(self, entry: Entry) -> None:
        entry.set_stopped()
        self._relink_playlist()

