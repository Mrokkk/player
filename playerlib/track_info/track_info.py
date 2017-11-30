#!/usr/bin/env python3

import logging
import os
import urwid
from time import gmtime, strftime

from playerlib.helpers.header import *
from playerlib.helpers.listbox_entry import *
from playerlib.helpers.scrollable_listbox import *
from playerlib.helpers.view_widget import *

class TrackInfo(ViewWidget):

    def __init__(self):
        self.header = Header('Track info')
        self.footer = urwid.AttrWrap(urwid.Text('Track info'), 'foot')
        self.content = urwid.SimpleListWalker([])
        self.listbox = urwid.ListBox(self.content)
        self._no_track_playing()
        super().__init__(self.listbox, {}, header=self.header)

    def _no_track_playing(self):
        self.content[:] = [urwid.Text('No track playing!')]

    def update(self, track):
        if track == None: return self._no_track_playing()
        self.content[:] = [
            urwid.Text('Artist: {}'.format(track.artist)),
            urwid.Text('Title: {}'.format(track.title)),
            urwid.Text('Index: {}'.format(track.index)),
            urwid.Text('Length: {}'.format(
                strftime('%M:%S', gmtime(track.length)))),
        ]

    def selectable(self):
        return False

