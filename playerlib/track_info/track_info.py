#!/usr/bin/env python3

import logging
import os
import urwim
from time import gmtime, strftime

class TrackInfo(urwim.ViewWidget):

    def __init__(self):
        self.header = urwim.Header('Track info')
        self.content = urwim.SimpleListWalker([])
        self.listbox = urwim.ListBox(self.content)
        self._no_track_playing()
        super().__init__(self.listbox, {}, 'Track info', header=self.header)
        urwim.rdb.subscribe('track', self._update)

    def _no_track_playing(self):
        self.content[:] = [urwim.Text('No track playing!')]

    def _update(self, track):
        if track == None: return self._no_track_playing()
        self.content[:] = [
            urwim.Text('Artist: {}'.format(track.artist)),
            urwim.Text('Title: {}'.format(track.title)),
            urwim.Text('Index: {}'.format(track.index)),
            urwim.Text('Length: {}'.format(
                strftime('%M:%S', gmtime(track.length)))),
        ]

    def selectable(self):
        return False

